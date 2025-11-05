#!/usr/bin/env python3
"""
Test específico para verificar el escenario completo de hundimiento
"""
import sys
sys.path.append('.')

from server import Ship, Player
import asyncio

def test_battleship_scenario():
    """Test que simula un escenario real de batalla naval"""
    print("=== TEST DE ESCENARIO BATALLA NAVAL ===")
    
    # Crear mock writer
    class MockWriter:
        def write(self, data): pass
        def drain(self): pass
        async def wait_closed(self): pass
        def close(self): pass
        def get_extra_info(self, key): return ('127.0.0.1', 12345)
    
    writer = MockWriter()
    player = Player("test_player", writer)
    
    # Colocar varios barcos como lo haría el cliente
    ships_data = [
        [(0, 0), (1, 0)],  # Barco de 2 casillas horizontal
        [(3, 3), (3, 4), (3, 5)],  # Barco de 3 casillas vertical  
        [(7, 7)]  # Barco de 1 casilla
    ]
    
    print("Colocando barcos:")
    for i, ship_positions in enumerate(ships_data):
        print(f"  Barco {i+1}: {ship_positions}")
        player.place_ship(ship_positions)
    
    print(f"\nTotal de barcos colocados: {len(player.ships)}")
    
    # Simular ataques para hundir el primer barco (2 casillas)
    print("\n=== ATACANDO PRIMER BARCO ===")
    print("Ataque a (0, 0):")
    result1 = player.receive_shot(0, 0)
    print(f"Resultado: {result1}")
    
    print("\nAtaque a (1, 0):")
    result2 = player.receive_shot(1, 0) 
    print(f"Resultado: {result2}")
    
    # Simular ataques para hundir el segundo barco (3 casillas)
    print("\n=== ATACANDO SEGUNDO BARCO ===")
    print("Ataque a (3, 3):")
    result3 = player.receive_shot(3, 3)
    print(f"Resultado: {result3}")
    
    print("\nAtaque a (3, 4):")
    result4 = player.receive_shot(3, 4)
    print(f"Resultado: {result4}")
    
    print("\nAtaque a (3, 5):")
    result5 = player.receive_shot(3, 5)
    print(f"Resultado: {result5}")
    
    # Atacar el tercer barco (1 casilla) 
    print("\n=== ATACANDO TERCER BARCO ===")
    print("Ataque a (7, 7):")
    result6 = player.receive_shot(7, 7)
    print(f"Resultado: {result6}")
    
    # Verificar si todos los barcos están hundidos
    print(f"\n¿Todos los barcos hundidos? {player.all_ships_sunk()}")
    
    print("\n=== FIN DEL TEST ===")

if __name__ == "__main__":
    test_battleship_scenario()