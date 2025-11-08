import asyncio
import logging
import sys
import os
from typing import List

# Importar ServerShip desde el mismo directorio
from server_ship import ServerShip

# Importar constantes y enums
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from constants import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from classes.enums import MessageType

logger = logging.getLogger(__name__)

class Player:
    def __init__(self, player_id: str, writer: asyncio.StreamWriter):
        self.player_id = player_id
        self.writer = writer
        self.ships_placed = False
        self.ready = False
        self.grid = [[CELL_EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # 0 = agua, 1 = barco, 2 = golpeado, 3 = agua golpeada
        self.ships = []  # Lista de objetos Ship
        
    async def send_message(self, message_type: MessageType, data=None):
        """Enviar mensaje al cliente"""
        try:
            import json
            message = {
                'type': message_type.value,
                'data': data
            }
            message_json = json.dumps(message) + '\n'
            self.writer.write(message_json.encode('utf-8'))
            await self.writer.drain()
            return True
        except ConnectionResetError:
            logger.error(f"🔌 Cliente {self.player_id} desconectado durante envío")
            return False
        except BrokenPipeError:
            logger.error(f"🔌 Conexión rota con {self.player_id}")
            return False
        except Exception as e:
            logger.error(f"❌ Error enviando mensaje a {self.player_id}: {e}")
            return False
    
    def place_ship(self, positions: List[tuple]):
        """Colocar un barco en el grid"""
        # Validar que todas las posiciones estén dentro del tablero
        valid_positions = []
        for x, y in positions:
            if MIN_COORDINATE <= x < GRID_SIZE and MIN_COORDINATE <= y < GRID_SIZE:
                self.grid[y][x] = CELL_SHIP
                valid_positions.append((x, y))
            else:
                logger.warning(f"Posición fuera del tablero ignorada: ({x}, {y})")
        
        if valid_positions:
            ship = ServerShip(valid_positions)
            self.ships.append(ship)
            logger.info(f"Barco colocado: {ship.ship_type} en posiciones {valid_positions}")
        else:
            logger.error("No se pudieron colocar posiciones válidas para el barco")
    
    def find_ship_containing(self, x: int, y: int):
        """Return the Ship that contains the coordinate (x,y).

        If no ship contains the coordinate, return None.
        """
        for ship in self.ships:
            if ship.contains_position(x, y):
                return ship
        return None
    
    def receive_shot(self, x: int, y: int) -> dict:
        """
        Procesar disparo recibido. 
        
        Returns:
            dict con 'result' ('hit', 'miss', 'sunk') y opcionalmente 'ship_info'
        """
        # Controlar que el tiro caiga en el tablero
        if not (MIN_COORDINATE <= x < GRID_SIZE and MIN_COORDINATE <= y < GRID_SIZE):
            logger.warning(f"Disparo fuera del tablero: ({x}, {y})")
            return {'result': 'miss'}
        
        # Verificar el estado actual de la celda
        current_cell = self.grid[y][x]
        
        if current_cell == CELL_EMPTY:  # Agua
            self.grid[y][x] = CELL_WATER_HIT  # Marcar agua como golpeada
            logger.info(f"Disparo al agua en ({x}, {y})")
            return {'result': 'miss'}
        
        if current_cell == CELL_SHIP:  # Barco no golpeado
            self.grid[y][x] = CELL_HIT  # Marcar como golpeado
            
            # Buscar el barco al que pertenecen las coordenadas
            ship = self.find_ship_containing(x, y)
            
            if ship is None:
                logger.error(f"ERROR: No se encontró barco en posición ({x}, {y}) que debería tener uno")
                return {'result': 'hit'}
            
            # Marcar la posición como golpeada en el barco
            ship.hit(x, y)
            logger.info(f"Golpe en {ship.ship_type} en posición ({x}, {y})")
            
            # Verificar si el barco está hundido
            if ship.is_sunk():
                logger.info(f"¡{ship.ship_type} hundido!")
                return {
                    'result': 'sunk',
                    'ship_info': {
                        'name': ship.ship_type,
                        'size': ship.size,
                        'positions': list(ship.positions)
                    }
                }
            else:
                return {'result': 'hit'}
        
        # Barco ya golpeado o agua ya golpeada
        logger.info(f"Disparo a posición ya golpeada: ({x}, {y})")
        return {'result': 'miss'}
    
    def all_ships_sunk(self) -> bool:
        """Verificar si todos los barcos fueron hundidos"""
        if not self.ships:
            return False
        return all(ship.is_sunk() for ship in self.ships)