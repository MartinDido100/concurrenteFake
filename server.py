import asyncio
import json
import logging
from typing import Dict, List, Optional, Set
from enum import Enum
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GameState(Enum):
    WAITING_PLAYERS = "waiting_players"
    PLACEMENT_PHASE = "placement_phase"
    BATTLE_PHASE = "battle_phase" 
    GAME_OVER = "game_over"

class MessageType(Enum):
    PLAYER_CONNECT = "player_connect"
    PLAYER_DISCONNECT = "player_disconnect"
    PLAYERS_READY = "players_ready"
    PLACE_SHIPS = "place_ships"
    SHOT = "shot"
    SHOT_RESULT = "shot_result"
    SHIP_SUNK = "ship_sunk"
    ENEMY_SHIP_SUNK = "enemy_ship_sunk"
    GAME_START = "game_start"
    GAME_UPDATE = "game_update"
    GAME_OVER = "game_over"
    ERROR = "error"

class Player:
    def __init__(self, player_id: str, writer: asyncio.StreamWriter):
        self.player_id = player_id
        self.writer = writer
        self.ships_placed = False
        self.ready = False
        self.grid = [[0 for _ in range(10)] for _ in range(10)]
        self.ships = []
        self.hits_received = set()
    async def send_message(self, message_type: MessageType, data=None):
        try:
            message = {
                'type': message_type.value,
                'data': data
            }
            message_json = json.dumps(message) + '\n'
            self.writer.write(message_json.encode('utf-8'))
            await self.writer.drain()
            return True
        except (ConnectionResetError, BrokenPipeError):
            logger.error(f"Cliente {self.player_id} desconectado durante envío")
            return False
        except Exception as e:
            logger.error(f"Error enviando mensaje a {self.player_id}: {e}")
            return False
    def place_ship(self, positions: List[tuple]):
        for x, y in positions:
            if 0 <= x < 10 and 0 <= y < 10:
                self.grid[y][x] = 1
        self.ships.append(positions)
    def receive_shot(self, x: int, y: int) -> tuple:
        if not (0 <= x < 10 and 0 <= y < 10):
            return ('miss', None)
        if self.grid[y][x] == 1:
            self.grid[y][x] = 2
            self.hits_received.add((x, y))
            
            for i, ship_positions in enumerate(self.ships):
                if (x, y) in ship_positions:
                    ship_hits = sum(1 for pos in ship_positions if pos in self.hits_received)
                    
                    if ship_hits >= len(ship_positions):
                        ship_name = self.get_ship_name_by_size(len(ship_positions))
                        return ('sunk', ship_name)
                    else:
                        return ('hit', None)
            
            return ('hit', None)
        else:
            if self.grid[y][x] == 0:
                self.grid[y][x] = 3
            return ('miss', None)
    
    def get_ship_name_by_size(self, size: int) -> str:
        names = {5: "Portaaviones", 4: "Destructor Acorazado", 3: "Barco de Ataque", 2: "Lancha Rapida"}
        return names.get(size, f"Barco de {size} casillas")
    
    def all_ships_sunk(self) -> bool:
        total_ship_positions = sum(len(ship) for ship in self.ships)
        return len(self.hits_received) == total_ship_positions

class BattleshipServer:
    def __init__(self, host='0.0.0.0', port=8889):
        self.host = host
        self.port = port
        self.players: Dict[str, Player] = {}
        self.max_players = 2
        self.game_state = GameState.WAITING_PLAYERS
        self.current_turn = None
        
    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        logger.info(f"Servidor iniciado en {self.host}:{self.port}")
        async with server:
            await server.serve_forever()
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client_addr = writer.get_extra_info('peername')
        player_id = str(uuid.uuid4())[:8]
        logger.info(f"Cliente conectado desde {client_addr}, ID: {player_id}")
        
        if len(self.players) >= self.max_players:
            await self.send_error(writer, "Servidor lleno. Máximo 2 jugadores.")
            writer.close()
            await writer.wait_closed()
            return
        
        player = Player(player_id, writer)
        self.players[player_id] = player
        await player.send_message(MessageType.PLAYER_CONNECT, {'player_id': player_id})
        await self.broadcast_players_status()
        
        try:
            while self.players.get(player_id) is not None:
                try:
                    line = await asyncio.wait_for(reader.readline(), timeout=1.0)
                    if not line:
                        break
                    
                    raw_data = line.decode('utf-8').strip()
                    if not raw_data:
                        continue
                    
                    message = json.loads(raw_data)
                    await self.process_message(player_id, message)
                    
                except asyncio.TimeoutError:
                    continue
                except (ConnectionResetError, json.JSONDecodeError):
                    break
                except Exception as e:
                    logger.error(f"Error procesando mensaje de {player_id}: {e}")
                    break
        
        except Exception as e:
            logger.error(f"Error en conexión con {player_id}: {e}")
        finally:
            await self.disconnect_player(player_id)
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass
    
    async def send_error(self, writer: asyncio.StreamWriter, error_message: str):
        """Enviar mensaje de error"""
        try:
            message = {
                'type': MessageType.ERROR.value,
                'data': {'error': error_message}
            }
            message_json = json.dumps(message) + '\n'
            writer.write(message_json.encode('utf-8'))
            await writer.drain()
        except Exception as e:
            logger.error(f"Error enviando mensaje de error: {e}")
    
    async def disconnect_player(self, player_id: str):
        if player_id in self.players:
            if self.game_state in [GameState.PLACEMENT_PHASE, GameState.BATTLE_PHASE] and len(self.players) == 2:
                other_player_id = next((pid for pid in self.players if pid != player_id), None)
                if other_player_id:
                    await self.players[other_player_id].send_message(MessageType.PLAYER_DISCONNECT, {
                        'disconnected_player': player_id,
                        'message': 'Tu oponente se ha desconectado',
                        'return_to_menu': True
                    })
            
            del self.players[player_id]
            
            if len(self.players) < 2:
                self.game_state = GameState.WAITING_PLAYERS
                self.current_turn = None
            
            await self.broadcast_players_status()
    
    async def broadcast_players_status(self):
        """Enviar estado de jugadores conectados a todos los clientes"""
        players_ready = len(self.players) >= 2
        message_data = {
            'connected_players': len(self.players),
            'max_players': self.max_players,
            'players_ready': players_ready,
            'game_state': self.game_state.value
        }
        
        for player in self.players.values():
            await player.send_message(MessageType.PLAYERS_READY, message_data)
    
    async def process_message(self, player_id: str, message: dict):
        """Procesar mensaje de un cliente"""
        message_type = message.get('type')
        data = message.get('data', {})
        
        logger.info(f"Mensaje recibido de {player_id}: {message_type}")

        if player_id not in self.players:
            return
        
        player = self.players[player_id]

        if message_type == 'place_ships':
            await self.handle_place_ships(player, data)
        elif message_type == 'shot':
            await self.handle_shot(player_id, data)
        elif message_type == 'start_game':
            await self.handle_start_game()
        else:
            logger.warning(f"Tipo de mensaje desconocido: {message_type}")
    
    async def handle_place_ships(self, player: Player, data: dict):
        """Manejar colocación de barcos"""
        try:
            ships_data = data.get('ships', [])
            
            # Limpiar barcos anteriores
            player.ships = []
            player.grid = [[0 for _ in range(10)] for _ in range(10)]
            
            # Colocar cada barco
            for ship_positions in ships_data:
                player.place_ship(ship_positions)
            
            player.ships_placed = True
            logger.info(f"Jugador {player.player_id} ha colocado sus barcos")
            
            # Verificar si ambos jugadores han colocado sus barcos
            if self.all_players_ready():
                await self.start_battle_phase()
            
        except Exception as e:
            logger.error(f"Error en colocación de barcos: {e}")
            await player.send_message(MessageType.ERROR, {'error': 'Error colocando barcos'})
    
    async def handle_shot(self, shooter_id: str, data: dict):
        if self.game_state != GameState.BATTLE_PHASE:
            return
        
        if self.current_turn != shooter_id:
            await self.players[shooter_id].send_message(
                MessageType.ERROR, {'error': 'No es tu turno'}
            )
            return
        
        x, y = data.get('x'), data.get('y')
        if not (isinstance(x, int) and isinstance(y, int)):
            return
        
        opponent_id = next((pid for pid in self.players if pid != shooter_id), None)
        if not opponent_id:
            return
        
        opponent = self.players[opponent_id]
        result, ship_name = opponent.receive_shot(x, y)
        
        shot_data = {
            'x': x, 'y': y, 'result': result,
            'shooter': shooter_id, 'target': opponent_id
        }
        
        if result == 'sunk' and ship_name:
            shot_data['sunk_ship_name'] = ship_name
        
        for player in self.players.values():
            await player.send_message(MessageType.SHOT_RESULT, shot_data)
        
        if result == 'sunk' and ship_name:
            victory_message = {
                'ship_name': ship_name,
                'message': f"¡HUNDISTE EL {ship_name.upper()}!",
                'position': {'x': x, 'y': y},
                'enemy_id': opponent_id
            }
            await self.players[shooter_id].send_message(MessageType.ENEMY_SHIP_SUNK, victory_message)
        
        if opponent.all_ships_sunk():
            await self.end_game(shooter_id)
        else:
            if result == 'miss':
                self.current_turn = opponent_id
            await self.broadcast_game_state()
    
    async def handle_start_game(self):
        if len(self.players) == 2:
            self.game_state = GameState.PLACEMENT_PHASE
            
            start_message = {
                'phase': 'placement',
                'message': 'El juego ha comenzado - Pantalla de juego activa',
                'redirect_to_game': True
            }
            
            for player in self.players.values():
                await player.send_message(MessageType.GAME_START, start_message)
    
    async def start_battle_phase(self):
        """Iniciar fase de batalla"""
        self.game_state = GameState.BATTLE_PHASE
        # Elegir jugador que empieza aleatoriamente
        import random
        player_ids = list(self.players.keys())
        self.current_turn = random.choice(player_ids)
        
        logger.info(f"Fase de batalla iniciada. Turno de: {self.current_turn}")
        
        await self.broadcast_game_state()
    
    async def broadcast_game_state(self):
        """Enviar estado del juego a todos los jugadores"""
        game_data = {
            'phase': self.game_state.value,
            'current_turn': self.current_turn,
            'players': {pid: {'ready': p.ships_placed} for pid, p in self.players.items()}
        }
        
        for player in self.players.values():
            await player.send_message(MessageType.GAME_UPDATE, game_data)
    
    async def end_game(self, winner_id: str):
        """Finalizar el juego"""
        self.game_state = GameState.GAME_OVER
        logger.info(f"Juego terminado. Ganador: {winner_id}")
        
        for player_id, player in self.players.items():
            is_winner = player_id == winner_id
            await player.send_message(MessageType.GAME_OVER, {
                'winner': winner_id,
                'is_winner': is_winner,
                'message': '¡Ganaste!' if is_winner else 'Perdiste'
            })
    
    def all_players_ready(self) -> bool:
        """Verificar si todos los jugadores están listos"""
        return (len(self.players) == 2 and 
                all(player.ships_placed for player in self.players.values()))

async def main():
    server = BattleshipServer()
    try:
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("Servidor detenido por el usuario")
    except Exception as e:
        logger.error(f"Error en el servidor: {e}")

if __name__ == "__main__":
    asyncio.run(main())