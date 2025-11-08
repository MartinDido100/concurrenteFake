"""
Punto de entrada principal para el cliente del juego Batalla Naval
"""

import pygame
import sys
import os

# Agregar el directorio padre al path para importar constants
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classes import BattleshipClient
from constants import *

if __name__ == "__main__":
    client = BattleshipClient()
    client.run()