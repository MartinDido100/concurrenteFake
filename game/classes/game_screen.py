"""
Pantalla principal del juego de Batalla Naval
Maneja la colocación de barcos y la fase de batalla
"""

import pygame
import os
import sys

# Importar constants y GameBoard desde las ubicaciones correctas
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from constants import *
from .game_board import GameBoard

class GameScreen:
    def __init__(self, screen, network_manager=None):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.network_manager = network_manager
        
        # Calcular tamaño para los tableros
        title_space = 80   # Espacio para título principal arriba
        board_title_space = 60  # Más espacio para títulos fuera de paneles
        info_space = 150   # Espacio para información abajo
        available_height = self.height - title_space - board_title_space - info_space
        available_width = self.width - 160  # Más margen para coordenadas
        
        # Separar mucho más los tableros para que no se toquen
        board_spacing = 150  # Separación mucho mayor
        max_board_width = (available_width - board_spacing) // 2
        max_board_height = available_height
        
        # Reducir el tamaño un 20% para dar más espacio de separación
        board_size = int(min(max_board_width, max_board_height) * 0.8)
        
        # Centrar los tableros horizontalmente y verticalmente
        total_width = board_size * 2 + board_spacing
        start_x = (self.width - total_width) // 2
        
        # Centrar verticalmente considerando todos los espacios
        total_board_area = board_size + board_title_space  # Tablero + espacio para su título
        available_vertical = self.height - title_space - info_space
        board_y = title_space + (available_vertical - total_board_area) // 2 + board_title_space
        
        self.my_board = GameBoard(start_x, board_y, board_size)
        self.enemy_board = GameBoard(start_x + board_size + board_spacing, board_y, board_size)
        
        self.game_phase = "placement"
        self.selected_ship_size = 2
        self.ship_horizontal = True
        self.my_turn = False
        
        self.ships_to_place = SHIP_SIZES.copy()
        self.current_ship_index = 0
        
        # Seguimiento de barcos enemigos hundidos
        self.enemy_sunk_ships = []
        self.enemy_sunk_ships_info = {}  # Diccionario para almacenar info completa de barcos hundidos
        
        self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)
        
        print("✅ Sistema de barcos realistas inicializado")
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_left_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.handle_right_click(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.ship_horizontal = not self.ship_horizontal
    
    def handle_left_click(self, mouse_pos):
        if self.game_phase == "placement" and self.current_ship_index < len(self.ships_to_place):
            cell = self.my_board.get_cell_from_mouse(mouse_pos)
            if cell:
                ship_size = self.ships_to_place[self.current_ship_index]
                if self.my_board.place_ship(ship_size, cell[0], cell[1], self.ship_horizontal):
                    self.current_ship_index += 1
                    if self.current_ship_index >= len(self.ships_to_place):
                        self.game_phase = "waiting_for_battle"
                        self.send_ships_to_server()
        
        elif self.game_phase == "battle" and self.my_turn:
            cell = self.enemy_board.get_cell_from_mouse(mouse_pos)
            if cell and cell not in self.enemy_board.shots and self.network_manager:
                self.network_manager.make_shot(cell[0], cell[1])
    
    def handle_right_click(self, mouse_pos):
        self.ship_horizontal = not self.ship_horizontal
    
    def update(self):
        pass
    
    def draw(self):
        self.draw_ocean_background()
        
        self.draw_board_panels()
        
        title_font = pygame.font.Font(None, FONT_SIZE_TITLE)
        title_text = title_font.render("BATALLA NAVAL", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(self.width // 2, 35))
        self.screen.blit(title_text, title_rect)
        
        board_font = pygame.font.Font(None, FONT_SIZE_BOARD_TITLE)
        
        # Posicionar títulos fuera del recuadro, con espacio de separación
        title_spacing = 15  # Espacio entre título y panel del tablero
        
        my_title = board_font.render("MI FLOTA", True, (255, 255, 255))
        my_panel_top = self.my_board.y - 40 - 15  # panel_padding + coord_space desde draw_board_panels
        my_title_rect = my_title.get_rect(center=(self.my_board.x + self.my_board.width // 2, my_panel_top - title_spacing))
        self.screen.blit(my_title, my_title_rect)
        
        enemy_title = board_font.render("ENEMIGO", True, (255, 255, 255))
        enemy_panel_top = self.enemy_board.y - 40 - 15  # panel_padding + coord_space desde draw_board_panels
        enemy_title_rect = enemy_title.get_rect(center=(self.enemy_board.x + self.enemy_board.width // 2, enemy_panel_top - title_spacing))
        self.screen.blit(enemy_title, enemy_title_rect)
        
        self.my_board.draw(self.screen, show_ships=True)
        self.draw_enemy_board_with_sunk_ships()
        
        # Dibujar estado de los barcos si estamos en batalla
        if self.game_phase == "battle" or self.game_phase == "waiting_for_battle":
            self.draw_ships_status()
        
        if self.game_phase == "placement" and self.current_ship_index < len(self.ships_to_place):
            mouse_pos = pygame.mouse.get_pos()
            cell = self.my_board.get_cell_from_mouse(mouse_pos)
            if cell:
                self.draw_ship_preview_realistic(cell[0], cell[1])
        
        self.draw_info_panel()
        
        # Fuentes más grandes para mejor legibilidad
        main_info_font = pygame.font.Font(None, 32)
        secondary_info_font = pygame.font.Font(None, 28)
        
        if self.game_phase == "placement":
            if self.current_ship_index < len(self.ships_to_place):
                ship_size = self.ships_to_place[self.current_ship_index]
                orientation = "Horizontal" if self.ship_horizontal else "Vertical"
                status_text = f"Colocando barco de tamaño {ship_size} ({orientation}) - Click derecho o R para rotar"
            else:
                status_text = "Todos los barcos colocados - Esperando al oponente..."
        elif self.game_phase == "battle":
            if self.my_turn:
                status_text = "¡Tu turno! Haz click en el tablero enemigo para disparar"
            else:
                status_text = "Turno del oponente - Espera tu turno..."
        elif self.game_phase == "waiting_for_battle":
            status_text = "Barcos colocados - Esperando que inicie la batalla..."
        else:
            status_text = "Preparando juego..."
        
        # Texto principal centrado en el panel
        status_surface = main_info_font.render(status_text, True, (255, 255, 255))
        status_rect = status_surface.get_rect(center=(self.width // 2, self.height - 75))
        self.screen.blit(status_surface, status_rect)
        
        # Información adicional
        if self.game_phase == "placement":
            remaining_ships = self.ships_to_place[self.current_ship_index:]
            if remaining_ships:
                ships_text = f"Barcos restantes: {remaining_ships}"
                ships_surface = secondary_info_font.render(ships_text, True, (200, 220, 255))
                ships_rect = ships_surface.get_rect(center=(self.width // 2, self.height - 45))
                self.screen.blit(ships_surface, ships_rect)

    
    def draw_ocean_background(self):
        for y in range(self.height):
            ratio = y / self.height
            r = int(30 + (70 - 30) * ratio)
            g = int(60 + (130 - 60) * ratio)  
            b = int(90 + (200 - 90) * ratio)
            color = (r, g, b)
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))
    
    def draw_board_panels(self):
        panel_padding = 15
        panel_color = (0, 0, 0, 100)
        border_color = (255, 255, 255, 150)
        
        coord_space = 40  # Espacio para las coordenadas
        
        my_panel = pygame.Rect(
            self.my_board.x - panel_padding - coord_space,
            self.my_board.y - panel_padding - coord_space,
            self.my_board.width + panel_padding * 2 + coord_space * 2,
            self.my_board.height + panel_padding * 2 + coord_space * 2
        )
        
        enemy_panel = pygame.Rect(
            self.enemy_board.x - panel_padding - coord_space,
            self.enemy_board.y - panel_padding - coord_space,
            self.enemy_board.width + panel_padding * 2 + coord_space * 2,
            self.enemy_board.height + panel_padding * 2 + coord_space * 2
        )
        
        my_panel_surface = pygame.Surface((my_panel.width, my_panel.height))
        my_panel_surface.set_alpha(100)
        my_panel_surface.fill((20, 40, 60))
        
        enemy_panel_surface = pygame.Surface((enemy_panel.width, enemy_panel.height))
        enemy_panel_surface.set_alpha(100)
        enemy_panel_surface.fill((40, 20, 20))
        
        self.screen.blit(my_panel_surface, (my_panel.x, my_panel.y))
        self.screen.blit(enemy_panel_surface, (enemy_panel.x, enemy_panel.y))
        
        pygame.draw.rect(self.screen, (100, 149, 237), my_panel, 3)
        pygame.draw.rect(self.screen, (220, 20, 60), enemy_panel, 3)
    
    def draw_info_panel(self):
        panel_height = 110
        panel_y = self.height - panel_height - 15
        
        info_panel = pygame.Rect(60, panel_y, self.width - 120, panel_height)
        info_surface = pygame.Surface((info_panel.width, info_panel.height))
        info_surface.set_alpha(130)
        info_surface.fill((25, 45, 85))
        
        self.screen.blit(info_surface, (info_panel.x, info_panel.y))
        pygame.draw.rect(self.screen, (120, 160, 255), info_panel, 3)
    
    def draw_ships_status(self):
        """Dibujar el estado de los barcos propios y enemigos"""
        ship_font = pygame.font.Font(None, 24)
        title_font = pygame.font.Font(None, 28)
        
        # Panel izquierdo para barcos propios
        left_panel_x = 10
        left_panel_y = self.my_board.y + 50
        left_panel_width = 200
        left_panel_height = 300
        
        # Panel derecho para barcos enemigos
        right_panel_x = self.width - 210
        right_panel_y = self.enemy_board.y + 50
        right_panel_width = 200
        right_panel_height = 300
        
        # Dibujar panel de mis barcos
        left_panel = pygame.Rect(left_panel_x, left_panel_y, left_panel_width, left_panel_height)
        left_surface = pygame.Surface((left_panel_width, left_panel_height))
        left_surface.set_alpha(180)
        left_surface.fill((20, 60, 40))
        self.screen.blit(left_surface, (left_panel_x, left_panel_y))
        pygame.draw.rect(self.screen, (100, 200, 120), left_panel, 2)
        
        # Título panel izquierdo
        my_title = title_font.render("MIS BARCOS", True, (255, 255, 255))
        self.screen.blit(my_title, (left_panel_x + 10, left_panel_y + 10))
        
        # Estado de mis barcos
        my_ships = self.my_board.get_ships_status()
        y_offset = 40
        for ship in my_ships:
            if ship['sunk']:
                color = (255, 100, 100)  # Rojo para hundidos
                status = "HUNDIDO"
            else:
                color = (100, 255, 100)  # Verde para activos
                status = f"{ship['hits']}/{ship['total_hits_needed']} impactos"
            
            ship_text = ship_font.render(f"• {ship['name']}", True, color)
            status_text = ship_font.render(f"  {status}", True, (200, 200, 200))
            
            self.screen.blit(ship_text, (left_panel_x + 10, left_panel_y + y_offset))
            self.screen.blit(status_text, (left_panel_x + 15, left_panel_y + y_offset + 18))
            y_offset += 45
        
        # Dibujar panel de barcos enemigos
        right_panel = pygame.Rect(right_panel_x, right_panel_y, right_panel_width, right_panel_height)
        right_surface = pygame.Surface((right_panel_width, right_panel_height))
        right_surface.set_alpha(180)
        right_surface.fill((60, 20, 20))
        self.screen.blit(right_surface, (right_panel_x, right_panel_y))
        pygame.draw.rect(self.screen, (200, 100, 100), right_panel, 2)
        
        # Título panel derecho
        enemy_title = title_font.render("BARCOS ENEMIGOS", True, (255, 255, 255))
        self.screen.blit(enemy_title, (right_panel_x + 10, right_panel_y + 10))
        
        # Estado de barcos enemigos (estimado basado en los hundidos conocidos)
        enemy_ships = self.get_enemy_ships_status()
        y_offset = 40
        for ship in enemy_ships:
            if ship['sunk']:
                color = (255, 100, 100)  # Rojo para hundidos
                status = "HUNDIDO"
            else:
                color = (255, 200, 100)  # Amarillo para desconocidos
                status = "ACTIVO"
            
            ship_text = ship_font.render(f"• {ship['name']}", True, color)
            status_text = ship_font.render(f"  {status}", True, (200, 200, 200))
            
            self.screen.blit(ship_text, (right_panel_x + 10, right_panel_y + y_offset))
            self.screen.blit(status_text, (right_panel_x + 15, right_panel_y + y_offset + 18))
            y_offset += 45
    
    def get_enemy_ships_status(self):
        """Obtener el estado estimado de los barcos enemigos"""
        # Lista de barcos que debería tener el enemigo
        expected_ships = [
            {"name": "Portaaviones", "size": 5, "sunk": False},
            {"name": "Destructor Acorazado", "size": 4, "sunk": False},
            {"name": "Barco de Ataque #1", "size": 3, "sunk": False},
            {"name": "Barco de Ataque #2", "size": 3, "sunk": False},
            {"name": "Lancha Rapida", "size": 2, "sunk": False}
        ]
        
        # Marcar como hundidos los barcos que están en nuestra lista
        for sunk_ship_name in self.enemy_sunk_ships:
            for ship in expected_ships:
                if ship['name'] == sunk_ship_name or (sunk_ship_name == "Barco de Ataque" and "Barco de Ataque" in ship['name'] and not ship['sunk']):
                    ship['sunk'] = True
                    break
        
        return expected_ships
    
    def draw_ship_preview_realistic(self, x, y):
        from .ship import Ship  # Import local para evitar dependencia circular
        
        ship_size = self.ships_to_place[self.current_ship_index]
        
        can_place = self.my_board.can_place_ship(ship_size, x, y, self.ship_horizontal)
        
        temp_ship = Ship(ship_size)
        temp_ship.horizontal = self.ship_horizontal
        
        for i in range(ship_size):
            if self.ship_horizontal:
                temp_ship.positions.append((x + i, y))
            else:
                temp_ship.positions.append((x, y + i))
        
        preview_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        preview_surface.set_alpha(60)  # Reducido de 120 a 60 para menos transparencia/oscuridad
        preview_surface.fill((0, 0, 0, 0))
        
        temp_board = GameBoard(self.my_board.x, self.my_board.y, self.my_board.width)
        temp_board.ships = [temp_ship]
        temp_board.colors = self.my_board.colors.copy()
        
        if can_place:
            temp_board.colors['ship'] = (0, 255, 0)  # Verde más brillante
        else:
            temp_board.colors['ship'] = (255, 50, 50)  # Rojo más brillante
        
        temp_board.draw_realistic_ship(preview_surface, temp_ship)
        
        self.screen.blit(preview_surface, (0, 0))
    
    def send_ships_to_server(self):
        if self.network_manager:
            ships_data = []
            for ship in self.my_board.ships:
                ships_data.append(ship.positions)
            
            self.network_manager.place_ships(ships_data)
            print("Barcos enviados al servidor")
    
    def handle_shot_result(self, data):
        x, y = data.get('x'), data.get('y')
        result = data.get('result')
        shooter = data.get('shooter')
        ship_info = data.get('ship_info')  # Información del barco hundido (si aplica)
        
        print(f"Disparo en ({x}, {y}) por jugador {shooter}: {result}")
        
        # Extraer nombre del barco si fue hundido
        sunk_ship_name = None
        if result == 'sunk' and ship_info:
            sunk_ship_name = ship_info.get('name')
            ship_size = ship_info.get('size')
            ship_positions = ship_info.get('positions', [])
            print(f"📊 Información del barco hundido: {sunk_ship_name} (tamaño: {ship_size})")

        if result == 'hit' or result == 'sunk':
            self.play_missile_sound()
        elif result == 'miss':
            self.play_water_splash_sound()
        
        if shooter == self.network_manager.player_id:
            # Mi disparo - registrar en el tablero enemigo
            self.enemy_board.shots[(x, y)] = result
            
            # Si hundí un barco enemigo, procesarlo completamente
            if result == 'sunk' and sunk_ship_name and ship_info:
                # Allow storing multiple sunk ships even if they have the same name
                # (e.g. two "Barco de Ataque"). We intentionally don't deduplicate by name.
                self.enemy_sunk_ships.append(sunk_ship_name)
                print(f"🎯 ¡HUNDISTE EL {sunk_ship_name.upper()} ENEMIGO!")

                # Almacenar información completa del barco para mostrar nombres en el tablero
                ship_positions = ship_info.get('positions', [])
                for pos in ship_positions:
                    self.enemy_sunk_ships_info[tuple(pos)] = sunk_ship_name

                # Marcar todas las posiciones del barco como hundidas (usar posiciones reales)
                self.enemy_board.mark_enemy_ship_sunk(ship_info, ship_positions)
            
            # Solo pierdo el turno si es miss
            if result == 'miss':
                self.my_turn = False
            # Si es hit o sunk, mantengo el turno para seguir disparando
            
        else:
            # El disparo fue del oponente hacia mi tablero
            # Registrar el disparo del enemigo en mi tablero propio
            self.my_board.shots[(x, y)] = result
            
            # Si fue hit, también marcar el barco como golpeado
            if result == 'hit' or result == 'sunk':
                for ship in self.my_board.ships:
                    if (x, y) in ship.positions:
                        ship.hit(x, y)
                        if ship.sunk and result == 'sunk':
                            print(f"💥 ¡El enemigo hundió tu {ship.name}!")
                        break
    
    def set_my_turn(self, is_my_turn):
        self.my_turn = is_my_turn
    
    def start_battle_phase(self):
        print("🚀 Iniciando fase de batalla...")
        self.game_phase = "battle"
    

    
    def draw_enemy_board_with_sunk_ships(self):
        """Dibujar el tablero enemigo sin etiquetas de barcos hundidos"""
        # Simplemente dibujar el tablero normal sin etiquetas
        self.enemy_board.draw(self.screen, show_ships=False)
    
    def play_missile_sound(self):
        """Reproducir sonido de impacto de misil"""
        try:
            missile_sound_path = os.path.join("assets", "sounds", "misil.mp3")
            missile_sound = pygame.mixer.Sound(missile_sound_path)
            missile_sound.set_volume(0.3)  # Volumen reducido al 30% para evitar saturación
            missile_sound.play()
            print("🔊 Reproduciendo sonido de impacto de misil")
        except pygame.error as e:
            print(f"❌ Error al reproducir sonido de misil: {e}")
        except FileNotFoundError:
            print("❌ No se encontró el archivo misil.mp3")
    
    def play_water_splash_sound(self):
        """Reproducir sonido de salpicadura de agua cuando se falla"""
        try:
            splash_sound_path = os.path.join("assets", "sounds", "waterSplash.mp3")
            splash_sound = pygame.mixer.Sound(splash_sound_path)
            splash_sound.set_volume(0.25)  # Volumen reducido al 25% para evitar saturación
            splash_sound.play()
            print("🔊 Reproduciendo sonido de salpicadura de agua")
        except pygame.error as e:
            print(f"❌ Error al reproducir sonido de salpicadura: {e}")
        except FileNotFoundError:
            print("❌ No se encontró el archivo waterSplash.mp3")

    def reset_game_state(self):
        """Resetear el estado de la pantalla de juego para una nueva partida.

        Esto limpia tableros, barcos, disparos y la información de barcos hundidos
        para evitar que queden residuos de la partida anterior en la UI.
        """
        # Reiniciar tableros completamente
        self.my_board = GameBoard(self.my_board.x, self.my_board.y, self.my_board.width)
        self.enemy_board = GameBoard(self.enemy_board.x, self.enemy_board.y, self.enemy_board.width)

        # Resetear estado de fase y colocación
        self.game_phase = "placement"
        self.selected_ship_size = 2
        self.ship_horizontal = True
        self.my_turn = False
        self.ships_to_place = [5, 4, 3, 3, 2]
        self.current_ship_index = 0

        # Limpiar seguimiento de barcos enemigos hundidos
        self.enemy_sunk_ships = []
        self.enemy_sunk_ships_info = {}

        # Fuentes se preservan
        print("🔄 Estado del juego reseteado para nueva partida")