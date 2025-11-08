"""
Clase Ship para el cliente de Batalla Naval
Maneja la representación visual y lógica del juego local
"""
import sys
import os

# Importar constants desde la carpeta padre del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from constants import SHIP_NAMES

class Ship:
    """
    Representa un barco en el cliente de Batalla Naval.
    Se inicializa con un tamaño y se posiciona en el tablero.
    """
    
    def __init__(self, size: int, ship_type: str = None):
        """
        Inicializar barco del cliente con tamaño.
        
        Args:
            size: Tamaño del barco (número de casillas)
            ship_type: Tipo de barco (opcional)
        """
        self.size = size
        self.positions = []
        self.hits = set()
        self.sunk = False
        self.horizontal = True
        self.ship_type = ship_type or self.get_ship_name_by_size(size)
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
        
        Returns:
            True si la posición pertenece al barco y fue golpeada
            False si la posición no pertenece al barco
        """
        if (x, y) in self.positions:
            self.hits.add((x, y))
            
            # Actualizar estado de hundido
            if self.is_sunk():
                self.sunk = True
            
            return True
        return False
    
    def is_sunk(self) -> bool:
        """Verificar si el barco está hundido (todas sus posiciones fueron golpeadas)"""
        if not self.positions:
            return False
        return len(self.hits) >= len(self.positions)
    
    def get_remaining_positions(self) -> set:
        """Obtener las posiciones del barco que aún no han sido golpeadas"""
        return set(self.positions) - self.hits
    
    # Métodos adicionales para el cliente
    def set_positions(self, positions):
        """Establecer las posiciones del barco (usado por game.py)"""
        self.positions = positions
        
    def add_position(self, x, y):
        """Agregar una posición al barco"""
        if (x, y) not in self.positions:
            self.positions.append((x, y))
    
    def set_horizontal(self, horizontal: bool):
        """Establecer orientación del barco"""
        self.horizontal = horizontal
    
    def __str__(self):
        """Representación en string del barco del cliente."""
        status = "Hundido" if self.sunk else f"{len(self.hits)}/{len(self.positions)} golpeado"
        return f"{self.ship_type} [{status}]"
    
    def __repr__(self):
        """Representación para debugging."""
        return f"Ship(size={self.size}, positions={self.positions}, hits={list(self.hits)})"