"""
Clase GameBoard para el cliente de Batalla Naval
Maneja el tablero de juego y la representación visual
"""
import pygame
import sys
import os

# Importar constants desde la carpeta padre del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from constants import *

# Importar Ship desde el mismo paquete
from .ship import Ship

class GameBoard:
    def __init__(self, x, y, board_size=BOARD_SIZE_DEFAULT):
        self.x = x
        self.y = y
        self.grid_size = GRID_SIZE
        self.width = board_size
        self.height = board_size
        self.cell_size = board_size // self.grid_size
        
        self.grid = [['empty' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.ships = []
        self.shots = {}
        
        self.colors = {
            'water': COLOR_WATER,
            'ship': SHIP_HULL_COLOR,
            'hit': COLOR_HIT,
            'miss': COLOR_MISS,
            'grid': COLOR_GRID,
            'hover': COLOR_HOVER,
            'water_dark': COLOR_WATER_DARK,
        }
    
    def draw(self, screen, show_ships=True):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell_x = self.x + col * self.cell_size
                cell_y = self.y + row * self.cell_size
                
                if (row + col) % 2 == 0:
                    color = self.colors['water']
                else:
                    color = self.colors['water_dark']
                
                pygame.draw.rect(screen, color,
                               (cell_x, cell_y, self.cell_size, self.cell_size))
        
        for i in range(self.grid_size + 1):
            line_width = 2 if i % 5 == 0 else 1
            
            pygame.draw.line(screen, self.colors['grid'], 
                           (self.x + i * self.cell_size, self.y),
                           (self.x + i * self.cell_size, self.y + self.height), line_width)
            pygame.draw.line(screen, self.colors['grid'],
                           (self.x, self.y + i * self.cell_size),
                           (self.x + self.width, self.y + i * self.cell_size), line_width)

        if show_ships:
            for ship in self.ships:
                self.draw_realistic_ship(screen, ship)
        
        for (shot_x, shot_y), result in self.shots.items():
            cell_x = self.x + shot_x * self.cell_size
            cell_y = self.y + shot_y * self.cell_size
            center_x = cell_x + self.cell_size // 2
            center_y = cell_y + self.cell_size // 2
            
            if result == 'hit' or result == 'sunk':
                # Misil rojo para aciertos (hit o sunk)
                self.draw_missile(screen, center_x, center_y, (220, 20, 60), 'hit')
            elif result == 'miss':
                # Misil blanco para fallos
                self.draw_missile(screen, center_x, center_y, (255, 255, 255), 'miss')
        
        # Dibujar coordenadas del tablero
        self.draw_coordinates(screen)
    
    def draw_missile(self, screen, center_x, center_y, color, shot_type):
        """Dibujar un misil realista en la posición del disparo"""
        if shot_type == 'hit':
            # Misil de impacto - más grande y con efectos de explosión
            missile_size = self.cell_size // MISSILE_SIZE_HIT
            
            # Cuerpo principal del misil (elipse vertical)
            missile_body = pygame.Rect(center_x - 8, center_y - 12, 16, 24)
            pygame.draw.ellipse(screen, color, missile_body)
            
            # Punta del misil
            points = [
                (center_x, center_y - 15),  # Punta superior
                (center_x - 6, center_y - 8),  # Izquierda
                (center_x + 6, center_y - 8)   # Derecha
            ]
            pygame.draw.polygon(screen, (180, 15, 45), points)
            
            # Aletas del misil
            pygame.draw.polygon(screen, (150, 10, 30), [
                (center_x - 8, center_y + 8),
                (center_x - 12, center_y + 15),
                (center_x - 4, center_y + 12)
            ])
            pygame.draw.polygon(screen, (150, 10, 30), [
                (center_x + 8, center_y + 8),
                (center_x + 12, center_y + 15),
                (center_x + 4, center_y + 12)
            ])
            
            # Efecto de explosión/fuego
            for i, explosion_color in enumerate(EXPLOSION_COLORS[:3]):
                explosion_radius = 6 - i * 2
                pygame.draw.circle(screen, explosion_color, 
                                 (center_x, center_y + 5), explosion_radius)
            
        else:  # miss
            # Misil de fallo - más pequeño, blanco/gris
            missile_size = self.cell_size // MISSILE_SIZE_MISS
            
            # Cuerpo principal del misil
            missile_body = pygame.Rect(center_x - 6, center_y - 10, 12, 20)
            pygame.draw.ellipse(screen, color, missile_body)
            
            # Punta del misil
            points = [
                (center_x, center_y - 12),  # Punta superior
                (center_x - 4, center_y - 6),  # Izquierda
                (center_x + 4, center_y - 6)   # Derecha
            ]
            pygame.draw.polygon(screen, (200, 200, 200), points)
            
            # Aletas del misil
            pygame.draw.polygon(screen, (180, 180, 180), [
                (center_x - 6, center_y + 6),
                (center_x - 9, center_y + 12),
                (center_x - 3, center_y + 10)
            ])
            pygame.draw.polygon(screen, (180, 180, 180), [
                (center_x + 6, center_y + 6),
                (center_x + 9, center_y + 12),
                (center_x + 3, center_y + 10)
            ])
            
            # Salpicadura de agua (círculos azules)
            for i, splash_color in enumerate(SPLASH_COLORS):
                splash_radius = 4 - i
                splash_y = center_y + 8 + i * 2
                pygame.draw.circle(screen, splash_color, 
                                 (center_x, splash_y), splash_radius)
    

    
    def draw_coordinates(self, screen):
        """Dibujar las coordenadas del tablero"""
        coord_font_size = max(MIN_COORD_FONT_SIZE, min(MAX_COORD_FONT_SIZE, self.cell_size // COORD_FONT_CELL_RATIO))
        coord_font = pygame.font.Font(None, coord_font_size)
        coord_bg_width = max(COORD_BG_MIN_WIDTH, self.cell_size // 3)
        coord_bg_height = max(COORD_BG_MIN_HEIGHT, self.cell_size // 4)
        
        for i in range(self.grid_size):
            # Números a la izquierda
            num_text = coord_font.render(str(i + 1), True, COLOR_WHITE)
            num_bg = pygame.Rect(self.x - coord_bg_width - COORD_BG_MARGIN, self.y + i * self.cell_size + (self.cell_size - coord_bg_height) // 2, coord_bg_width, coord_bg_height)
            pygame.draw.rect(screen, (50, 80, 120), num_bg)
            pygame.draw.rect(screen, COLOR_WHITE, num_bg, 1)
            text_rect = num_text.get_rect(center=num_bg.center)
            screen.blit(num_text, text_rect)
            
            # Letras arriba
            letter = chr(ord('A') + i)
            letter_text = coord_font.render(letter, True, COLOR_WHITE)
            letter_bg = pygame.Rect(self.x + i * self.cell_size + (self.cell_size - coord_bg_width) // 2, self.y - coord_bg_height - COORD_BG_MARGIN, coord_bg_width, coord_bg_height)
            pygame.draw.rect(screen, (50, 80, 120), letter_bg)
            pygame.draw.rect(screen, COLOR_WHITE, letter_bg, 1)
            text_rect = letter_text.get_rect(center=letter_bg.center)
            screen.blit(letter_text, text_rect)
    
    def draw_realistic_ship(self, screen, ship):
        if not ship.positions:
            return
        
        # Colores base más realistas
        hull_color = SHIP_HULL_COLOR  # Gris azulado oscuro
        deck_color = SHIP_DECK_COLOR  # Madera
        metal_color = SHIP_METAL_COLOR  # Metal
        cannon_color = SHIP_CANNON_COLOR  # Negro metálico
        detail_color = SHIP_DETAIL_COLOR  # Detalles dorados
        window_color = SHIP_WINDOW_COLOR  # Ventanas azules
        hit_color = COLOR_RED
        
        margin = CELL_MARGIN
        
        min_x = min(pos[0] for pos in ship.positions)
        max_x = max(pos[0] for pos in ship.positions)
        min_y = min(pos[1] for pos in ship.positions)
        max_y = max(pos[1] for pos in ship.positions)
        
        start_pixel_x = self.x + min_x * self.cell_size + margin
        start_pixel_y = self.y + min_y * self.cell_size + margin
        
        if ship.horizontal:
            ship_width = (max_x - min_x + 1) * self.cell_size - 2 * margin
            ship_height = self.cell_size - 2 * margin
            
            # Casco principal con degradado
            hull_rect = pygame.Rect(start_pixel_x, start_pixel_y + 6, ship_width, ship_height - 12)
            pygame.draw.ellipse(screen, hull_color, hull_rect)
            
            # Línea de agua (más clara)
            water_line = pygame.Rect(start_pixel_x, start_pixel_y + hull_rect.height - 4, ship_width, 8)
            pygame.draw.ellipse(screen, SHIP_WATER_LINE_COLOR, water_line)
            
            # Cubierta principal
            deck_rect = pygame.Rect(start_pixel_x + 4, start_pixel_y + 8, ship_width - 8, ship_height - 20)
            pygame.draw.ellipse(screen, deck_color, deck_rect)
            
            # Superestructura según el tamaño del barco
            self.draw_ship_superstructure(screen, ship, start_pixel_x, start_pixel_y, ship_width, ship_height, True)
            
        else:  # Vertical
            ship_width = self.cell_size - 2 * margin
            ship_height = (max_y - min_y + 1) * self.cell_size - 2 * margin
            
            # Casco principal
            hull_rect = pygame.Rect(start_pixel_x + 6, start_pixel_y, ship_width - 12, ship_height)
            pygame.draw.ellipse(screen, hull_color, hull_rect)
            
            # Línea de agua
            water_line = pygame.Rect(start_pixel_x + hull_rect.width - 4, start_pixel_y, 8, ship_height)
            pygame.draw.ellipse(screen, SHIP_WATER_LINE_COLOR, water_line)
            
            # Cubierta principal
            deck_rect = pygame.Rect(start_pixel_x + 8, start_pixel_y + 4, ship_width - 20, ship_height - 8)
            pygame.draw.ellipse(screen, deck_color, deck_rect)
            
            # Superestructura según el tamaño del barco
            self.draw_ship_superstructure(screen, ship, start_pixel_x, start_pixel_y, ship_width, ship_height, False)
        
        # Dibujar impactos de balas si los hay
        for pos_x, pos_y in ship.positions:
            if (pos_x, pos_y) in ship.hits:
                hit_x = self.x + pos_x * self.cell_size + self.cell_size // 2
                hit_y = self.y + pos_y * self.cell_size + self.cell_size // 2
                
                # Efecto de explosión más dramático
                for i, color in enumerate(EXPLOSION_COLORS):
                    radius = 12 - i * 3
                    pygame.draw.circle(screen, color, (hit_x, hit_y), radius)
    
    def draw_ship_superstructure(self, screen, ship, start_x, start_y, width, height, horizontal):
        """Dibujar la superestructura específica según el tipo de barco"""
        # Colores para detalles
        metal_color = SHIP_METAL_COLOR
        cannon_color = SHIP_CANNON_COLOR
        detail_color = SHIP_DETAIL_COLOR
        window_color = SHIP_WINDOW_COLOR
        radar_color = SHIP_RADAR_COLOR
        
        if ship.size == 5:  # Portaaviones
            self.draw_aircraft_carrier(screen, start_x, start_y, width, height, horizontal)
        elif ship.size == 4:  # Destructor
            self.draw_destroyer(screen, start_x, start_y, width, height, horizontal)
        elif ship.size == 3:  # Barco de Ataque
            self.draw_attack_ship(screen, start_x, start_y, width, height, horizontal)
        elif ship.size == 2:  # Lancha Táctica
            self.draw_tactical_boat(screen, start_x, start_y, width, height, horizontal)
    
    def draw_aircraft_carrier(self, screen, start_x, start_y, width, height, horizontal):
        """Dibujar portaaviones con cubierta de vuelo y torre de control"""
        if horizontal:
            # Cubierta de vuelo
            flight_deck = pygame.Rect(start_x + 5, start_y + 5, width - 10, 8)
            pygame.draw.rect(screen, (90, 90, 90), flight_deck)
            
            # Torre de control (isla)
            tower_x = start_x + width * 0.7
            tower = pygame.Rect(tower_x, start_y + 8, 15, 20)
            pygame.draw.rect(screen, (70, 70, 70), tower)
            
            # Antenas de radar
            pygame.draw.line(screen, (200, 200, 200), (tower_x + 7, start_y + 8), (tower_x + 7, start_y + 3), 2)
            pygame.draw.circle(screen, (100, 255, 100), (tower_x + 7, start_y + 3), 3)
            
            # Líneas de la cubierta
            for i in range(3):
                line_x = start_x + 10 + i * (width - 20) // 3
                pygame.draw.line(screen, (70, 70, 70), (line_x, start_y + 6), (line_x, start_y + 12), 1)
        else:
            # Versión vertical del portaaviones
            flight_deck = pygame.Rect(start_x + 5, start_y + 5, 8, height - 10)
            pygame.draw.rect(screen, (90, 90, 90), flight_deck)
            
            tower_y = start_y + height * 0.3
            tower = pygame.Rect(start_x + 8, tower_y, 20, 15)
            pygame.draw.rect(screen, (70, 70, 70), tower)
    
    def draw_destroyer(self, screen, start_x, start_y, width, height, horizontal):
        """Dibujar destructor con cañones y sistemas de defensa"""
        if horizontal:
            # Torreta principal delantera
            turret1_x = start_x + width * 0.2
            pygame.draw.circle(screen, (60, 60, 60), (turret1_x, start_y + height // 2), 8)
            # Cañón principal
            cannon_end_x = turret1_x + 15
            pygame.draw.line(screen, (40, 40, 40), (turret1_x, start_y + height // 2), 
                           (cannon_end_x, start_y + height // 2), 4)
            
            # Torreta trasera
            turret2_x = start_x + width * 0.8
            pygame.draw.circle(screen, (60, 60, 60), (turret2_x, start_y + height // 2), 6)
            cannon_end_x2 = turret2_x - 12
            pygame.draw.line(screen, (40, 40, 40), (turret2_x, start_y + height // 2), 
                           (cannon_end_x2, start_y + height // 2), 3)
            
            # Puente de mando
            bridge_x = start_x + width * 0.5
            bridge = pygame.Rect(bridge_x - 8, start_y + 8, 16, 12)
            pygame.draw.rect(screen, (80, 80, 80), bridge)
            
            # Ventanas del puente
            for i in range(3):
                window_x = bridge_x - 6 + i * 4
                pygame.draw.rect(screen, (100, 150, 200), (window_x, start_y + 10, 2, 3))
        else:
            # Versión vertical
            turret1_y = start_y + height * 0.2
            pygame.draw.circle(screen, (60, 60, 60), (start_x + width // 2, turret1_y), 8)
            
            turret2_y = start_y + height * 0.8
            pygame.draw.circle(screen, (60, 60, 60), (start_x + width // 2, turret2_y), 6)
    
    def draw_attack_ship(self, screen, start_x, start_y, width, height, horizontal):
        """Dibujar barco de ataque con misiles y cañones menores"""
        if horizontal:
            # Cañón principal
            gun_x = start_x + width * 0.3
            pygame.draw.circle(screen, (50, 50, 50), (gun_x, start_y + height // 2), 6)
            pygame.draw.line(screen, (35, 35, 35), (gun_x, start_y + height // 2), 
                           (gun_x + 10, start_y + height // 2), 3)
            
            # Lanzamisiles
            missile_x = start_x + width * 0.7
            missile_rect = pygame.Rect(missile_x - 4, start_y + height // 2 - 3, 8, 6)
            pygame.draw.rect(screen, (70, 70, 70), missile_rect)
            
            # Superestructura
            super_rect = pygame.Rect(start_x + width * 0.4, start_y + 6, width * 0.3, 14)
            pygame.draw.rect(screen, (75, 75, 75), super_rect)
        else:
            # Versión vertical
            gun_y = start_y + height * 0.3
            pygame.draw.circle(screen, (50, 50, 50), (start_x + width // 2, gun_y), 6)
            
            missile_y = start_y + height * 0.7
            missile_rect = pygame.Rect(start_x + width // 2 - 3, missile_y - 4, 6, 8)
            pygame.draw.rect(screen, (70, 70, 70), missile_rect)
    
    def draw_tactical_boat(self, screen, start_x, start_y, width, height, horizontal):
        """Dibujar lancha táctica pequeña y ágil"""
        if horizontal:
            # Cañón pequeño
            gun_x = start_x + width * 0.4
            pygame.draw.circle(screen, (45, 45, 45), (gun_x, start_y + height // 2), 4)
            pygame.draw.line(screen, (30, 30, 30), (gun_x, start_y + height // 2), 
                           (gun_x + 8, start_y + height // 2), 2)
            
            # Cabina
            cabin = pygame.Rect(start_x + width * 0.6, start_y + 8, width * 0.3, 10)
            pygame.draw.rect(screen, (70, 70, 70), cabin)
            
            # Ventana
            pygame.draw.rect(screen, (100, 150, 200), (start_x + width * 0.65, start_y + 10, 4, 3))
        else:
            # Versión vertical
            gun_y = start_y + height * 0.4
            pygame.draw.circle(screen, (45, 45, 45), (start_x + width // 2, gun_y), 4)
            
            cabin = pygame.Rect(start_x + 8, start_y + height * 0.6, 10, height * 0.3)
            pygame.draw.rect(screen, (70, 70, 70), cabin)
    
    def get_cell_from_mouse(self, mouse_pos):
        mx, my = mouse_pos
        if (self.x <= mx <= self.x + self.width and 
            self.y <= my <= self.y + self.height):
            cell_x = (mx - self.x) // self.cell_size
            cell_y = (my - self.y) // self.cell_size
            if 0 <= cell_x < self.grid_size and 0 <= cell_y < self.grid_size:
                return (cell_x, cell_y)
        return None
    
    def can_place_ship(self, ship_size, start_x, start_y, horizontal=True):
        positions = []
        
        for i in range(ship_size):
            if horizontal:
                x, y = start_x + i, start_y
            else:
                x, y = start_x, start_y + i
            
            if x >= self.grid_size or y >= self.grid_size:
                return False
            
            for ship in self.ships:
                if (x, y) in ship.positions:
                    return False
            
            positions.append((x, y))
        
        return True
    
    def place_ship(self, ship_size, start_x, start_y, horizontal=True):
        if self.can_place_ship(ship_size, start_x, start_y, horizontal):
            ship = Ship(ship_size)
            ship.horizontal = horizontal
            
            for i in range(ship_size):
                if horizontal:
                    x, y = start_x + i, start_y
                else:
                    x, y = start_x, start_y + i
                ship.positions.append((x, y))
            
            self.ships.append(ship)
            return True
        return False
    
    def get_ships_status(self):
        """Obtener el estado de todos los barcos"""
        ships_status = []
        for ship in self.ships:
            status = {
                'name': ship.name,
                'size': ship.size,
                'sunk': ship.sunk,
                'hits': len(ship.hits),
                'total_hits_needed': ship.size
            }
            ships_status.append(status)
        return ships_status
    
    def get_sunk_ship_name(self, x, y):
        """Obtener el nombre del barco hundido en la posición dada"""
        # Para barcos propios
        for ship in self.ships:
            if (x, y) in ship.positions and ship.sunk:
                return ship.name
        return None
    

    
    def mark_enemy_ship_sunk(self, ship_info, shot_positions):
        """Marcar un barco enemigo como hundido basándose en la información del servidor"""
        if not ship_info:
            return
        
        ship_name = ship_info.get('name')
        ship_size = ship_info.get('size') 
        ship_positions = ship_info.get('positions', [])
        
        # Marcar todas las posiciones del barco como 'sunk' en el tablero enemigo
        for pos_x, pos_y in ship_positions:
            self.shots[(pos_x, pos_y)] = 'sunk'
        
        print(f"🎯 Barco enemigo {ship_name} marcado como hundido en posiciones: {ship_positions}")