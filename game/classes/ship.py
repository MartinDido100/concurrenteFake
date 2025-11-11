"""
Clase Ship unificada para Batalla Naval
Puede ser usada tanto por el cliente como por el servidor
"""
import sys
import os
import logging
from typing import List, Tuple, Set, Union

# Importar constants desde la carpeta padre del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from constants import SHIP_NAMES

logger = logging.getLogger(__name__)

class Ship:
    """
    Representa un barco en Batalla Naval.
    Puede inicializarse de dos formas:
    1. Con un tamaño (para el cliente, antes de colocar)
    2. Con posiciones específicas (para el servidor o después de colocar)
    """
    
    def __init__(self, size: int = None, ship_type: str = None, positions: List[Tuple[int, int]] = None):
        """
        Inicializar barco con tamaño o posiciones.
        
        Args:
            size: Tamaño del barco (número de casillas) - usado por el cliente
            ship_type: Tipo de barco (opcional)
            positions: Lista de tuplas (x, y) con las coordenadas del barco - usado por el servidor
        """
        # Inicialización por posiciones (modo servidor)
        if positions is not None:
            if not positions:
                raise ValueError("Las posiciones no pueden estar vacías")
            self.positions = list(positions)
            self.size = len(positions)
            self.ship_type = ship_type or self.get_ship_name_by_size(self.size)
            logger.debug(f"Ship creado con posiciones: {self.ship_type} en {self.positions}")
        
        # Inicialización por tamaño (modo cliente)
        elif size is not None:
            self.size = size
            self.positions = []
            self.ship_type = ship_type or self.get_ship_name_by_size(size)
        
        else:
            raise ValueError("Debe proporcionar 'size' o 'positions' para inicializar el barco")
        
        self.hits = set()
        self.sunk = False
        self.horizontal = True
        self.name = self.ship_type  # Alias para compatibilidad
    
    def get_ship_name_by_size(self, size: int) -> str:
        """Obtener el nombre del barco según su tamaño"""
        return SHIP_NAMES.get(size, f"Barco de {size} casillas")
    
    def contains_position(self, x: int, y: int) -> bool:
        """Verificar si el barco contiene la posición (x, y)"""
        return (x, y) in self.positions
    
    def hit(self, x: int, y: int) -> bool:
        """
        Marcar una posición como golpeada si pertenece al barco.
        
        Args:
            x: Coordenada X del golpe
            y: Coordenada Y del golpe
        
        Returns:
            True si la posición pertenece al barco y fue golpeada
            False si la posición no pertenece al barco
        """
        if (x, y) in self.positions:
            self.hits.add((x, y))
            logger.debug(f"Golpe registrado en {self.ship_type} en posición ({x}, {y})")
            
            # Actualizar estado de hundido
            if self.is_sunk():
                self.sunk = True
                logger.debug(f"{self.ship_type} está hundido")
            
            return True
        return False
    
    def is_sunk(self) -> bool:
        """Verificar si el barco está hundido (todas sus posiciones fueron golpeadas)"""
        if not self.positions:
            return False
        return len(self.hits) >= len(self.positions)
    
    def get_remaining_positions(self) -> Set[Tuple[int, int]]:
        """Obtener las posiciones del barco que aún no han sido golpeadas"""
        return set(self.positions) - self.hits
    
    def get_hit_positions(self) -> Set[Tuple[int, int]]:
        """
        Obtener las posiciones del barco que han sido golpeadas.
        
        Returns:
            Set de tuplas con las posiciones golpeadas
        """
        return self.hits.copy()
    
    # Métodos adicionales para el cliente
    def set_positions(self, positions):
        """Establecer las posiciones del barco (usado por el cliente al colocar barcos)"""
        self.positions = positions
        
    def add_position(self, x, y):
        """Agregar una posición al barco"""
        if (x, y) not in self.positions:
            self.positions.append((x, y))
    
    def set_horizontal(self, horizontal: bool):
        """Establecer orientación del barco"""
        self.horizontal = horizontal
    
    def __str__(self):
        """Representación en string del barco."""
        status = "Hundido" if self.sunk or self.is_sunk() else f"{len(self.hits)}/{len(self.positions)} golpeado"
        return f"{self.ship_type} [{status}]"
    
    def __repr__(self):
        """Representación para debugging."""
        return f"Ship(size={self.size}, type={self.ship_type}, positions={self.positions}, hits={list(self.hits)})"