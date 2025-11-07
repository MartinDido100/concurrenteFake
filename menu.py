import pygame
import os
from constants import *

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Cargar imagen de fondo del menú
        self.load_assets()
        
        # Estados del menú
        self.server_connected = False
        self.players_ready = False
        self.music_muted = False
        
        # Definir botones
        self.setup_buttons()
        
    def load_assets(self):
        try:
            # Cargar imagen de menú
            menu_path = os.path.join("assets", "images", "menu.png")
            self.menu_image = pygame.image.load(menu_path)
            self.menu_image = pygame.transform.scale(self.menu_image, (self.width, self.height))
        except pygame.error:
            # Si no se puede cargar la imagen, usar un fondo de color
            self.menu_image = None
            print("No se pudo cargar menu.png, usando fondo de color")
    
    def setup_buttons(self):
        # Configurar botones
        button_width = MENU_BUTTON_WIDTH
        button_height = MENU_BUTTON_HEIGHT
        center_x = self.width // 2
        
        # Botón "Conectar a servidor"
        self.connect_button = {
            'rect': pygame.Rect(center_x - button_width // 2, MENU_BUTTON_Y_CONNECT, button_width, button_height),
            'text': 'Conectar a Servidor',
            'enabled': True,
            'color': COLOR_BUTTON_CONNECT,
            'hover_color': COLOR_BUTTON_CONNECT_HOVER,
            'text_color': COLOR_WHITE
        }
        
        # Botón "Iniciar partida"
        self.start_button = {
            'rect': pygame.Rect(center_x - button_width // 2, MENU_BUTTON_Y_START, button_width, button_height),
            'text': 'Iniciar Partida',
            'enabled': False,  # Se habilita cuando hay 2 jugadores
            'color': COLOR_BUTTON_START,
            'hover_color': COLOR_BUTTON_START_HOVER,
            'disabled_color': COLOR_BUTTON_DISABLED,
            'text_color': COLOR_WHITE
        }
        
        # Botón de mute (esquina superior derecha)
        self.mute_button = {
            'rect': pygame.Rect(self.width - MUTE_BUTTON_WIDTH - MUTE_BUTTON_MARGIN, MUTE_BUTTON_MARGIN, MUTE_BUTTON_WIDTH, MUTE_BUTTON_HEIGHT),
            'text': 'Silenciar',
            'text_muted': 'Musica',
            'color': COLOR_BUTTON_MUTE,
            'hover_color': COLOR_BUTTON_MUTE_HOVER,
            'text_color': COLOR_WHITE
        }
        
        self.buttons = [self.connect_button, self.start_button]
        self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)
        self.mute_font = pygame.font.Font(None, FONT_SIZE_SMALL)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.connect_button['rect'].collidepoint(mouse_pos) and self.connect_button['enabled']:
                return "connect"
            
            if self.start_button['rect'].collidepoint(mouse_pos) and self.start_button['enabled']:
                return "start_game"
            
            if self.mute_button['rect'].collidepoint(mouse_pos):
                return "toggle_music"
        
        return None
    
    def update(self):
        # Actualizar estado de los botones basado en conexión
        pass
    
    def draw_background(self):
        # Dibujar fondo
        if self.menu_image:
            self.screen.blit(self.menu_image, (0, 0))
        else:
            self.screen.fill((30, 30, 60))

    def draw_button(self, button, color):
        # Dibujar botón
        pygame.draw.rect(self.screen, color, button['rect'])
        pygame.draw.rect(self.screen, COLOR_WHITE, button['rect'], 3)
            
        # Dibujar texto del botón
        text_surface = self.font.render(button['text'], True, button['text_color'])
        text_rect = text_surface.get_rect(center=button['rect'].center)
        self.screen.blit(text_surface, text_rect)

    def update_connection_status(self):
        """Actualizar estado de botones y texto según conexión"""
        if self.server_connected:
            # Cambiar texto y deshabilitar botón conectar si ya estamos conectados
            self.connect_button['text'] = 'Conectado'
            self.connect_button['enabled'] = False
            self.connect_button['color'] = COLOR_BUTTON_CONNECT_ACTIVE  # Verde
            
            if self.players_ready:
                status_text = "¡2 jugadores conectados! Listo para iniciar"
                status_color = COLOR_GREEN
                self.start_button['enabled'] = True
            else:
                status_text = "Conectado - Esperando segundo jugador..."
                status_color = COLOR_YELLOW
                self.start_button['enabled'] = False
        else:
            self.connect_button['text'] = 'Conectar a Servidor'
            self.connect_button['enabled'] = True
            self.connect_button['color'] = COLOR_BUTTON_CONNECT  # Azul original
            status_text = "Desconectado del servidor"
            status_color = (255, 100, 100)
            self.start_button['enabled'] = False
        
        return status_text, status_color

    def render_all_buttons(self, mouse_pos):
        """Renderizar todos los botones del menú"""
        for button in self.buttons:
            # Determinar color del botón
            if not button['enabled']:
                color = button.get('disabled_color', (100, 100, 100))
            elif button['rect'].collidepoint(mouse_pos):
                color = button['hover_color']
            else:
                color = button['color']
            
            # Dibujar botón
            self.draw_button(button, color)

    def draw(self):

        self.draw_background()

        # Dibujar botones
        mouse_pos = pygame.mouse.get_pos()
        self.render_all_buttons(mouse_pos)
        
        # Actualizar texto y estado de botones según conexión
        status_text, status_color = self.update_connection_status()
        
        # Mostrar estado de conexión
        status_font = pygame.font.Font(None, FONT_SIZE_NORMAL)
        
        status_surface = status_font.render(status_text, True, status_color)
        status_rect = status_surface.get_rect(center=(self.width // 2, MENU_STATUS_Y))
        self.screen.blit(status_surface, status_rect)
        
        # Dibujar botón de música
        self.draw_mute_button(mouse_pos)
        
    
    def draw_mute_button(self, mouse_pos):
        """Dibujar el botón de control de música"""
        # Determinar color del botón
        if self.mute_button['rect'].collidepoint(mouse_pos):
            color = self.mute_button['hover_color']
        else:
            color = self.mute_button['color']
        
        # Dibujar botón
        pygame.draw.rect(self.screen, color, self.mute_button['rect'])
        pygame.draw.rect(self.screen, COLOR_WHITE, self.mute_button['rect'], 2)
        
        # Determinar texto según estado
        if self.music_muted:
            text = self.mute_button['text_muted']
        else:
            text = self.mute_button['text']
        
        # Dibujar texto del botón
        text_surface = self.mute_font.render(text, True, self.mute_button['text_color'])
        text_rect = text_surface.get_rect(center=self.mute_button['rect'].center)
        self.screen.blit(text_surface, text_rect)
    
    def toggle_music_mute(self):
        """Alternar entre silenciar y reproducir la música"""
        self.music_muted = not self.music_muted
        volume = MUTED_VOLUME if self.music_muted else MUSIC_VOLUME_MENU
        pygame.mixer.music.set_volume(volume)
        status = "🔇 Música silenciada" if self.music_muted else "🔊 Música reactivada"
        print(status)
    
    def set_connection_status(self, connected, players_ready=False):
        """Actualizar el estado de conexión desde el cliente principal"""
        self.server_connected = connected
        self.players_ready = players_ready