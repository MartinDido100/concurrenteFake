#!/usr/bin/env python3
"""
Script de prueba para verificar la lógica de los barcos
"""
import sys
sys.path.append('.')

# Importar las clases del servidor
from server import Ship, Player
import asyncio

def test_ship_sinking():
    """Test para verificar que los barcos se hunden correctamente"""
    print("=== TEST DE HUNDIMIENTO DE BARCOS ===")
    
    # Crear un barco de 2 casillas
    positions = [(2, 3), (3, 3)]
    ship = Ship(positions)
    
    print(f"Barco creado: {ship.ship_type}")
    print(f"Posiciones: {ship.positions}")
    print(f"¿Está hundido inicialmente? {ship.is_sunk()}")
    
    # Golpear primera posición
    print("\n--- Golpeando primera posición (2, 3) ---")
    hit1 = ship.hit(2, 3)
    print(f"Hit exitoso: {hit1}")
    print(f"Posiciones golpeadas: {ship.hit_positions}")
    print(f"¿Está hundido? {ship.is_sunk()}")
    
    # Golpear segunda posición
    print("\n--- Golpeando segunda posición (3, 3) ---")
    hit2 = ship.hit(3, 3)
    print(f"Hit exitoso: {hit2}")
    print(f"Posiciones golpeadas: {ship.hit_positions}")
    print(f"¿Está hundido? {ship.is_sunk()}")
    
    print("\n=== FIN DEL TEST ===")

def test_player_ship_interaction():
    """Test completo con Player"""
    print("\n=== TEST DE PLAYER CON BARCOS ===")
    
    # Crear un mock writer
    class MockWriter:
        def write(self, data): pass
        def drain(self): pass
        async def wait_closed(self): pass
        def close(self): pass
        def get_extra_info(self, key): return ('127.0.0.1', 12345)
    
    # Crear jugador
    writer = MockWriter()
    player = Player("test_player", writer)
    
    # Colocar un barco pequeño
    print("Colocando barco en [(1, 1), (1, 2)]")
    player.place_ship([(1, 1), (1, 2)])
    
    print(f"Barcos colocados: {len(player.ships)}")
    if player.ships:
        ship = player.ships[0]
        print(f"Primer barco - Tipo: {ship.ship_type}")
        print(f"Posiciones: {ship.positions}")
    
    # Verificar grid - recordar que grid[y][x]
    print(f"Grid en (1, 1) -> grid[1][1]: {player.grid[1][1]}")
    print(f"Grid en (1, 2) -> grid[2][1]: {player.grid[2][1]}")
    print(f"También verificar grid[1][2]: {player.grid[1][2]}")
    
    # Probar disparos
    print("\n--- Disparo a (1, 1) ---")
    result1 = player.receive_shot(1, 1)
    print(f"Resultado: {result1}")
    
    print("\n--- Disparo a (1, 2) ---")
    result2 = player.receive_shot(1, 2)
    print(f"Resultado: {result2}")
    
    print("\n=== FIN DEL TEST DE PLAYER ===")

if __name__ == "__main__":
    test_ship_sinking()
    test_player_ship_interaction()