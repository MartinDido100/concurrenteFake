import pygame
import sys
import os
from menu import MenuScreen
from game import GameScreen
from network import NetworkManager
from connection_dialog import ConnectionDialog

class GameOverScreen:
    def __init__(self, screen, is_winner=False):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.is_winner = is_winner
        
        # Configurar botón
        button_width = 200
        button_height = 60
        self.accept_button = {
            'rect': pygame.Rect(self.width // 2 - button_width // 2, self.height // 2 + 100, button_width, button_height),
            'text': 'ACEPTAR',
            'color': (70, 130, 180),
            'hover_color': (100, 149, 237),
            'text_color': (255, 255, 255)
        }
        
        self.font_large = pygame.font.Font(None, 96)
        self.font_medium = pygame.font.Font(None, 48)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo
                mouse_pos = pygame.mouse.get_pos()
                if self.accept_button['rect'].collidepoint(mouse_pos):
                    return "accept"
        return None
    
    def draw(self):
        # Fondo semi-transparente
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Texto principal
        if self.is_winner:
            main_text = "GANASTE"
            text_color = (0, 255, 0)  # Verde
        else:
            main_text = "PERDISTE"
            text_color = (255, 0, 0)  # Rojo
        
        # Dibujar texto principal
        text_surface = self.font_large.render(main_text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
        
        # Sombra del texto
        shadow_surface = self.font_large.render(main_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.width // 2 + 3, self.height // 2 - 47))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(text_surface, text_rect)
        
        # Dibujar botón
        mouse_pos = pygame.mouse.get_pos()
        button_color = self.accept_button['hover_color'] if self.accept_button['rect'].collidepoint(mouse_pos) else self.accept_button['color']
        
        pygame.draw.rect(self.screen, button_color, self.accept_button['rect'])
        pygame.draw.rect(self.screen, (255, 255, 255), self.accept_button['rect'], 3)
        
        # Texto del botón
        button_text = self.font_medium.render(self.accept_button['text'], True, self.accept_button['text_color'])
        button_text_rect = button_text.get_rect(center=self.accept_button['rect'].center)
        self.screen.blit(button_text, button_text_rect)

class BattleshipClient:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        self.min_width = 1200
        self.min_height = 800
        initial_width = self.min_width
        initial_height = self.min_height
        pygame.display.set_caption("Batalla Naval - Cliente")
        self.screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
        pygame.display.flip()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.clock = pygame.time.Clock()
        self.current_state = "menu"
        self.running = True
        self.network_manager = NetworkManager()
        

        
        # Inicializar pantallas
        self.menu_screen = MenuScreen(self.screen)
        self.game_screen = GameScreen(self.screen, self.network_manager)
        self.game_over_screen = None  # Se creará cuando sea necesario
        
        # Configurar callbacks de red
        self.setup_network_callbacks()
        
        # Inicializar música de fondo
        self.init_background_music()
    
    def init_background_music(self):
        """Inicializar y reproducir música de fondo"""
        try:
            music_path = os.path.join("assets", "sounds", "piratas.mp3")
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except (pygame.error, FileNotFoundError):
            pass

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Aplicar tamaño mínimo para evitar que los barcos se vean mal
                    new_width = max(event.w, self.min_width)
                    new_height = max(event.h, self.min_height)
                    
                    # Actualizar dimensiones cuando se redimensiona la ventana
                    self.width = new_width
                    self.height = new_height
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                    
                    # Preservar el estado del juego antes de recrear las pantallas
                    if hasattr(self, 'game_screen') and self.current_state == "game":
                        # Guardar el estado actual del juego incluyendo audio
                        saved_game_state = {
                            'game_phase': self.game_screen.game_phase,
                            'current_ship_index': self.game_screen.current_ship_index,
                            'ship_horizontal': self.game_screen.ship_horizontal,
                            'my_turn': self.game_screen.my_turn,
                            'my_ships': self.game_screen.my_board.ships.copy() if hasattr(self.game_screen, 'my_board') else [],
                            'enemy_shots': self.game_screen.enemy_board.shots.copy() if hasattr(self.game_screen, 'enemy_board') else {}
                        }
                        
                        # Recrear la pantalla de juego con las nuevas dimensiones
                        self.game_screen = GameScreen(self.screen, self.network_manager)
                        
                        # Restaurar el estado del juego
                        self.game_screen.game_phase = saved_game_state['game_phase']
                        self.game_screen.current_ship_index = saved_game_state['current_ship_index']
                        self.game_screen.ship_horizontal = saved_game_state['ship_horizontal']
                        self.game_screen.my_turn = saved_game_state['my_turn']
                        
                        # Restaurar los barcos colocados
                        self.game_screen.my_board.ships = saved_game_state['my_ships']
                        
                        # Restaurar los disparos del enemigo
                        self.game_screen.enemy_board.shots = saved_game_state['enemy_shots']
                    else:
                        # Si no estamos en el juego, recrear normalmente
                        self.game_screen = GameScreen(self.screen, self.network_manager)
                    
                    # Actualizar el menú
                    self.menu_screen = MenuScreen(self.screen)
                    self.setup_network_callbacks()
                    
                    # Recrear game over screen si existe
                    if self.game_over_screen is not None:
                        is_winner = self.game_over_screen.is_winner
                        self.game_over_screen = GameOverScreen(self.screen, is_winner)
                    
                # Manejar eventos según el estado actual
                if self.current_state == "menu":
                    action = self.menu_screen.handle_event(event)
                    if action == "connect":
                        # Mostrar diálogo de configuración de conexión
                        connection_dialog = ConnectionDialog(self.screen)
                        connection_config = connection_dialog.run()
                        
                        if connection_config:
                            host = connection_config['host']
                            port = connection_config['port']
                            
                            if self.network_manager.connect_to_server(host, port):
                                pass
                            else:
                                pass
                        else:
                            pass
                            
                    elif action == "start_game":
                        if self.network_manager.start_game():
                            pass
                    elif action == "toggle_music":
                        # Alternar música
                        self.menu_screen.toggle_music_mute()
                        
                elif self.current_state == "game":
                    self.game_screen.handle_event(event)
                elif self.current_state == "game_over":
                    action = self.game_over_screen.handle_event(event)
                    if action == "accept":
                        if self.network_manager.connected:
                            self.network_manager.disconnect()
                        
                        # Reiniciar completamente el game_screen para limpiar datos de partida anterior
                        self.game_screen = None
                        
                        self.menu_screen.set_connection_status(False, False)
                        self.init_background_music()
                        
                        if hasattr(self.menu_screen, 'music_muted') and self.menu_screen.music_muted:
                            pygame.mixer.music.set_volume(0.0)
                        
                        self.current_state = "menu"
                        self.game_over_screen = None
            
            if self.current_state != "menu" and hasattr(self.network_manager, 'connected'):
                if not self.network_manager.connected and self.current_state in ["game", "game_over"]:
                    self.on_server_disconnect()
            
            if self.current_state == "menu":
                self.menu_screen.update()
                self.menu_screen.draw()
            elif self.current_state == "game":
                self.game_screen.update()
                self.game_screen.draw()
            elif self.current_state == "game_over":
                self.game_screen.update()
                self.game_screen.draw()
                self.game_over_screen.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # Limpieza al cerrar
        if self.network_manager and self.network_manager.connected:
            self.network_manager.disconnect()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()
    
    def setup_network_callbacks(self):
        """Configurar callbacks para eventos de red"""
        self.network_manager.set_players_ready_callback(self.on_players_ready)
        self.network_manager.set_game_start_callback(self.on_game_start)
        self.network_manager.set_game_update_callback(self.on_game_update)
        self.network_manager.set_shot_result_callback(self.on_shot_result)
        self.network_manager.set_ship_sunk_callback(self.on_ship_sunk)  # Nuevo callback
        self.network_manager.set_enemy_ship_sunk_callback(self.on_enemy_ship_sunk)  # Nuevo callback
        self.network_manager.set_game_over_callback(self.on_game_over)
        self.network_manager.set_server_disconnect_callback(self.on_server_disconnect)
    
    def on_players_ready(self, data):
        connected = data.get('connected_players', 0) > 0
        players_ready = data.get('players_ready', False)
        self.menu_screen.set_connection_status(connected, players_ready)
    
    def on_game_start(self, data):
        pygame.mixer.music.stop()
        
        try:
            game_music_path = os.path.join("assets", "sounds", "background.mp3")
            pygame.mixer.music.load(game_music_path)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        except (pygame.error, FileNotFoundError):
            pass
        
        # Crear una nueva instancia de GameScreen para cada partida
        self.game_screen = GameScreen(self.screen, self.network_manager)
        
        self.current_state = "game"
    
    def on_game_update(self, data):
        phase = data.get('phase')
        current_turn = data.get('current_turn')
        
        if phase == 'battle_phase':
            self.game_screen.start_battle_phase()
            is_my_turn = current_turn == self.network_manager.player_id
            self.game_screen.set_my_turn(is_my_turn)
    
    def on_shot_result(self, data):
        if hasattr(self.game_screen, 'handle_shot_result'):
            self.game_screen.handle_shot_result(data)
    
    def on_ship_sunk(self, data):
        ship_name = data.get('ship_name', 'Barco desconocido')
        message = data.get('message', f'¡Hundiste un {ship_name}!')
        
        if self.current_state == "game" and self.game_screen:
            self.game_screen.add_temporary_message(f"🚢💥 ¡BARCO HUNDIDO! 💥🚢", 8.0, (255, 0, 0))
            self.game_screen.add_temporary_message(f"🏆 {message} 🏆", 6.0, (255, 215, 0))
    
    def on_enemy_ship_sunk(self, data):
        ship_name = data.get('ship_name', 'Barco enemigo')
        message = data.get('message', f'¡Hundiste el {ship_name}!')
        
        if self.current_state == "game" and self.game_screen:
            self.game_screen.add_temporary_message(f"🎯 {message} 🎯", 8.0, (255, 215, 0))
            self.game_screen.add_temporary_message(f"🏆 ¡VICTORIA! ¡BARCO DESTRUIDO! 🏆", 6.0, (0, 255, 0))
            print(f"❌ No se pudo mostrar mensaje de victoria")
    
    def on_game_over(self, data):
        """Callback cuando termina el juego"""
        print(f"Juego terminado: {data}")
        
        # Detener música de juego
        pygame.mixer.music.stop()
        print("🔇 Música de juego detenida")
        
        is_winner = data.get('is_winner', False)
        self.game_over_screen = GameOverScreen(self.screen, is_winner)
        self.current_state = "game_over"
    
    def on_server_disconnect(self):
        pygame.mixer.music.stop()
        
        self.network_manager.connected = False
        self.network_manager.player_id = None
        
        # Reiniciar completamente el game_screen para limpiar datos de partida anterior
        self.game_screen = None
        
        self.menu_screen.set_connection_status(False, False)
        
        self.init_background_music()
        
        if hasattr(self.menu_screen, 'music_muted') and self.menu_screen.music_muted:
            pygame.mixer.music.set_volume(0.0)
        
        self.current_state = "menu"
        self.game_over_screen = None
        
        print("✅ Redirigido al menú principal")

if __name__ == "__main__":
    client = BattleshipClient()
    client.run()