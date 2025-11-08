"""
Clase ServerShip para el servidor de Batalla Naval
Maneja la lógica de barcos en el lado del servidor
"""
import logging
from typing import List, Tuple, Set

logger = logging.getLogger(__name__)

class ServerShip:
    """
    Representa un barco en el servidor de Batalla Naval.
    Se inicializa con una lista de posiciones específicas.
    """
    
    # Mapeo de tamaño a nombre del barco
    SHIP_NAMES = {
        5: "Portaaviones",
        4: "Acorazado", 
        3: "Crucero",
        2: "Destructor",
        1: "Submarino"
    }
    
    def __init__(self, positions: List[Tuple[int, int]]):
        """
        Inicializar barco del servidor con posiciones específicas.
        
        Args:
            positions: Lista de tuplas (x, y) con las coordenadas del barco
        """
        if not positions:
            raise ValueError("Las posiciones no pueden estar vacías")
            
        self.positions: Set[Tuple[int, int]] = set(positions)
        self.hits: Set[Tuple[int, int]] = set()
        self.size = len(positions)
        self.ship_type = self.SHIP_NAMES.get(self.size, f"Barco de {self.size}")
        
        logger.debug(f"ServerShip creado: {self.ship_type} en posiciones {list(self.positions)}")
    
    def contains_position(self, x: int, y: int) -> bool:
        """
        Verificar si el barco contiene la posición dada.
        
        Args:
            x: Coordenada X
            y: Coordenada Y
            
        Returns:
            True si el barco contiene la posición, False en caso contrario
        """
        return (x, y) in self.positions
    
    def hit(self, x: int, y: int) -> bool:
        """
        Marcar una posición como golpeada.
        
        Args:
            x: Coordenada X del golpe
            y: Coordenada Y del golpe
            
        Returns:
            True si el golpe fue válido (posición del barco), False en caso contrario
        """
        if (x, y) in self.positions:
            self.hits.add((x, y))
            logger.debug(f"Golpe registrado en {self.ship_type} en posición ({x}, {y})")
            return True
        return False
    
    def is_sunk(self) -> bool:
        """
        Verificar si el barco está completamente hundido.
        
        Returns:
            True si todas las posiciones del barco han sido golpeadas
        """
        is_sunk = len(self.hits) == len(self.positions)
        if is_sunk:
            logger.debug(f"{self.ship_type} está hundido")
        return is_sunk
    
    def get_remaining_positions(self) -> Set[Tuple[int, int]]:
        """
        Obtener las posiciones del barco que aún no han sido golpeadas.
        
        Returns:
            Set de tuplas con las posiciones no golpeadas
        """
        return self.positions - self.hits
    
    def get_hit_positions(self) -> Set[Tuple[int, int]]:
        """
        Obtener las posiciones del barco que han sido golpeadas.
        
        Returns:
            Set de tuplas con las posiciones golpeadas
        """
        return self.hits.copy()
    
    def __str__(self):
        """Representación en string del barco del servidor."""
        status = "Hundido" if self.is_sunk() else f"{len(self.hits)}/{len(self.positions)} golpeado"
        return f"{self.ship_type} [{status}] en {list(self.positions)}"
    
    def __repr__(self):
        """Representación para debugging."""
        return f"ServerShip(positions={list(self.positions)}, hits={list(self.hits)})"