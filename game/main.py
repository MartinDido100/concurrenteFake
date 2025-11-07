import pygame
import sys
import os
from menu import MenuScreen
from game import GameScreen
from network import NetworkManager
from connection_dialog import ConnectionDialog
from constants import *

class GameOverScreen:
    def __init__(self, screen, is_winner=False):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.is_winner = is_winner
        
        # Configurar botón
        button_width = GAME_OVER_BUTTON_WIDTH
        button_height = GAME_OVER_BUTTON_HEIGHT
        self.accept_button = {
            'rect': pygame.Rect(self.width // 2 - button_width // 2, self.height // 2 + 100, button_width, button_height),
            'text': 'ACEPTAR',
            'color': COLOR_BUTTON_CONNECT,
            'hover_color': COLOR_BUTTON_CONNECT_HOVER,
            'text_color': COLOR_WHITE
        }
        
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_DIALOG_TITLE)
    
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
        overlay.set_alpha(GAME_OVER_ALPHA)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Determinar texto y color
        main_text = "GANASTE" if self.is_winner else "PERDISTE"
        text_color = COLOR_GREEN if self.is_winner else COLOR_RED
        
        # Dibujar texto principal con sombra
        shadow_surface = self.font_large.render(main_text, True, COLOR_BLACK)
        text_surface = self.font_large.render(main_text, True, text_color)
        
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
        shadow_rect = shadow_surface.get_rect(center=(self.width // 2 + 3, self.height // 2 - 47))
        
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(text_surface, text_rect)
        
        # Dibujar botón
        mouse_pos = pygame.mouse.get_pos()
        button_color = self.accept_button['hover_color'] if self.accept_button['rect'].collidepoint(mouse_pos) else self.accept_button['color']
        
        pygame.draw.rect(self.screen, button_color, self.accept_button['rect'])
        pygame.draw.rect(self.screen, COLOR_WHITE, self.accept_button['rect'], 3)
        
        # Texto del botón
        button_text = self.font_medium.render(self.accept_button['text'], True, self.accept_button['text_color'])
        button_text_rect = button_text.get_rect(center=self.accept_button['rect'].center)
        self.screen.blit(button_text, button_text_rect)

class BattleshipClient:
    def __init__(self):
        pygame.init()
        
        # Inicializar mixer de pygame para audio con configuración optimizada
        pygame.mixer.pre_init(frequency=MIXER_FREQUENCY, size=MIXER_SIZE, channels=MIXER_CHANNELS, buffer=MIXER_BUFFER)
        pygame.mixer.init()
        
        # Definir tamaño mínimo de ventana para que los barcos se vean correctamente
        self.min_width = MIN_WINDOW_WIDTH
        self.min_height = MIN_WINDOW_HEIGHT
        
        # Definir tamaño inicial de ventana (no pantalla completa)
        initial_width = INITIAL_WINDOW_WIDTH
        initial_height = INITIAL_WINDOW_HEIGHT
        
        # Establecer el título antes de crear la ventana
        pygame.display.set_caption("Batalla Naval - Cliente")
        
        # Crear ventana redimensionable con todos los controles (minimizar, restaurar/maximizar, cerrar)
        self.screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
        
        # Forzar la actualización de la ventana para asegurar que la barra de título aparezca
        pygame.display.flip()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.clock = pygame.time.Clock()
        
        # Estados del juego
        self.current_state = "menu"
        self.running = True
        
        # Inicializar network manager primero
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
            # Cargar y reproducir la música de fondo en bucle
            music_path = os.path.join("assets", "sounds", "piratas.mp3")
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(MUSIC_VOLUME_MENU)  # Volumen reducido para evitar saturación
            pygame.mixer.music.play(-1)  # -1 significa bucle infinito
            print("✅ Música de fondo 'piratas.mp3' iniciada")
        except pygame.error as e:
            print(f"❌ Error al cargar música de fondo: {e}")
        except FileNotFoundError:
            print("❌ No se encontró el archivo piratas.mp3")

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
                            # Intentar conectar con la configuración ingresada
                            host = connection_config['host']
                            port = connection_config['port']
                            
                            print(f"🔌 Intentando conectar al servidor...")
                            print(f"   Host: {host}")
                            print(f"   Puerto: {port}")
                            
                            if self.network_manager.connect_to_server(host, port):
                                print(f"✅ Conectado exitosamente a {host}:{port}")
                            else:
                                print(f"❌ Error: No se pudo conectar a {host}:{port}")
                        else:
                            print("❌ Conexión cancelada por el usuario")
                            
                    elif action == "start_game":
                        # Solicitar inicio del juego al servidor
                        if self.network_manager.start_game():
                            print("Solicitando inicio de partida...")
                    elif action == "toggle_music":
                        # Alternar música
                        self.menu_screen.toggle_music_mute()
                        
                elif self.current_state == "game":
                    self.game_screen.handle_event(event)
                elif self.current_state == "game_over":
                    action = self.game_over_screen.handle_event(event)
                    if action == "accept":
                        # Desconectar del servidor al terminar el juego
                        if self.network_manager.connected:
                            self.network_manager.disconnect()
                            print("Desconectado del servidor después del juego")
                        
                        # Resetear estado del menú para mostrar desconectado
                        self.menu_screen.set_connection_status(False, False)
                        
                        # Reiniciar música de fondo del menú
                        self.init_background_music()
                        
                        # Restaurar el estado de silencio si estaba activado
                        if hasattr(self.menu_screen, 'music_muted') and self.menu_screen.music_muted:
                            pygame.mixer.music.set_volume(MUTED_VOLUME)
                        
                        # Volver al menú
                        self.current_state = "menu"
                        self.game_over_screen = None
            
            # Verificar estado de conexión periódicamente si no estamos en el menú
            if self.current_state != "menu" and hasattr(self.network_manager, 'connected'):
                if not self.network_manager.connected and self.current_state in ["game", "game_over"]:
                    print("🔌 Detección de desconexión en bucle principal")
                    self.on_server_disconnect()
            
            # Renderizar según el estado actual
            if self.current_state == "menu":
                self.menu_screen.update()
                self.menu_screen.draw()
            elif self.current_state == "game":
                self.game_screen.update()
                self.game_screen.draw()
            elif self.current_state == "game_over":
                # Dibujar el juego de fondo y encima la pantalla de game over
                self.game_screen.update()
                self.game_screen.draw()
                self.game_over_screen.draw()
            
            pygame.display.flip()
            self.clock.tick(TARGET_FPS)
        
        # Detener música antes de cerrar
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
        self.network_manager.set_game_over_callback(self.on_game_over)
        self.network_manager.set_server_disconnect_callback(self.on_server_disconnect)
    
    def on_players_ready(self, data):
        """Callback cuando cambia el estado de jugadores conectados"""
        connected = data.get('connected_players', 0) > 0
        players_ready = data.get('players_ready', False)
        self.menu_screen.set_connection_status(connected, players_ready)
    
    def on_game_start(self, data):
        """Callback cuando inicia el juego"""
        print(f"🎮 MENSAJE GAME_START RECIBIDO: {data}")
        print("✅ El servidor confirmó el inicio del juego")
        print("🚀 Redirigiendo AMBOS clientes a la pantalla de juego...")
        
        # Detener completamente la música del menú
        pygame.mixer.music.stop()
        print("🔇 Música del menú detenida")
        
        # Cargar y reproducir música de fondo del juego
        try:
            game_music_path = os.path.join("assets", "sounds", "background.mp3")
            pygame.mixer.music.load(game_music_path)
            pygame.mixer.music.set_volume(MUSIC_VOLUME_GAME)  # Volumen reducido para evitar saturación
            pygame.mixer.music.play(-1)  # -1 significa bucle infinito
            print("🎵 Música de fondo del juego 'background.mp3' iniciada")
        except pygame.error as e:
            print(f"❌ Error al cargar música de juego: {e}")
        except FileNotFoundError:
            print("❌ No se encontró el archivo background.mp3")
        
        # Resetear la pantalla de juego para asegurarnos de que no quede nada de partidas previas
        if hasattr(self, 'game_screen') and self.game_screen is not None:
            try:
                self.game_screen.reset_game_state()
            except Exception as e:
                print(f"⚠️ Error reseteando pantalla de juego: {e}")

        # Cambiar automáticamente a la pantalla de juego (pantalla en blanco inicialmente)
        self.current_state = "game"
        print("✅ Estado cambiado a 'game' - Pantalla de juego activa")
    
    def on_game_update(self, data):
        """Callback para actualizaciones del juego"""
        # Actualizar estado del juego según los datos del servidor
        phase = data.get('phase')
        current_turn = data.get('current_turn')
        
        if phase == 'battle_phase':
            self.game_screen.start_battle_phase()
            # Verificar si es mi turno
            is_my_turn = current_turn == self.network_manager.player_id
            self.game_screen.set_my_turn(is_my_turn)
    
    def on_shot_result(self, data):
        """Callback para resultados de disparos"""
        # Actualizar tableros con resultado del disparo
        if hasattr(self.game_screen, 'handle_shot_result'):
            self.game_screen.handle_shot_result(data)
    
    def on_game_over(self, data):
        """Callback cuando termina el juego"""
        print(f"Juego terminado: {data}")
        
        # Detener música de juego
        pygame.mixer.music.stop()
        print("🔇 Música de juego detenida")
        
        # Obtener si el jugador ganó o perdió
        is_winner = data.get('is_winner', False)
        
        # Resetear la pantalla de juego para limpiar lo que quedó en pantalla
        if hasattr(self, 'game_screen') and self.game_screen is not None:
            try:
                self.game_screen.reset_game_state()
            except Exception as e:
                print(f"⚠️ Error reseteando pantalla tras game over: {e}")

        # Crear pantalla de game over
        self.game_over_screen = GameOverScreen(self.screen, is_winner)
        
        # Cambiar al estado de game over
        self.current_state = "game_over"
    
    def on_server_disconnect(self):
        """Callback cuando se desconecta el servidor o un jugador"""
        if self.current_state in ["game", "game_over"]:
            print("🔌 Oponente desconectado - Redirigiendo al menú principal")
        else:
            print("🔌 Servidor desconectado - Redirigiendo al menú principal")
        
        # Detener cualquier música que esté reproduciéndose
        pygame.mixer.music.stop()
        print("🔇 Música detenida por desconexión")
        
        # Marcar como desconectado en el manager
        self.network_manager.connected = False
        self.network_manager.player_id = None
        
        # Resetear estado del menú para mostrar desconectado
        self.menu_screen.set_connection_status(False, False)
        
        # Reiniciar música de fondo del menú
        self.init_background_music()
        
        # Restaurar el estado de silencio si estaba activado
        if hasattr(self.menu_screen, 'music_muted') and self.menu_screen.music_muted:
            pygame.mixer.music.set_volume(MUTED_VOLUME)
        
        # Volver al menú principal
        self.current_state = "menu"
        self.game_over_screen = None
        
        print("✅ Redirigido al menú principal")

if __name__ == "__main__":
    client = BattleshipClient()
    client.run()