"""
Diálogo de configuración de conexión para el juego Batalla Naval
Permite elegir entre LAN (localhost) u Online (ngrok)
"""

import pygame
import sys

class ConnectionDialog:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Estado del diálogo
        self.active = True
        self.result = None  # {'mode': 'lan'/'online', 'host': str, 'port': int}
        
        # Modos de conexión
        self.connection_mode = 'lan'  # 'lan' o 'online'
        
        # Campos de texto
        self.host_input = 'localhost'
        self.port_input = '8888'
        self.active_input = 'host'  # 'host' o 'port'
        
        # Fuentes
        self.font_title = pygame.font.Font(None, 48)
        self.font_normal = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Configurar elementos de UI
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar elementos de la interfaz"""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Botones de modo de conexión
        button_width = 250
        button_height = 60
        button_spacing = 30
        
        self.lan_button = {
            'rect': pygame.Rect(center_x - button_width - button_spacing//2, center_y - 150, button_width, button_height),
            'text': 'LAN (Local)',
            'mode': 'lan',
            'color': (70, 130, 180),
            'hover_color': (100, 149, 237),
            'selected_color': (34, 139, 34)
        }
        
        self.online_button = {
            'rect': pygame.Rect(center_x + button_spacing//2, center_y - 150, button_width, button_height),
            'text': 'Online (ngrok)',
            'mode': 'online',
            'color': (70, 130, 180),
            'hover_color': (100, 149, 237),
            'selected_color': (34, 139, 34)
        }
        
        # Campos de entrada
        input_width = 400
        input_height = 50
        
        self.host_field = {
            'rect': pygame.Rect(center_x - input_width//2, center_y - 30, input_width, input_height),
            'label': 'Host / IP:',
            'name': 'host',
            'color': (200, 200, 200),
            'active_color': (255, 255, 255),
            'text_color': (0, 0, 0)
        }
        
        self.port_field = {
            'rect': pygame.Rect(center_x - input_width//2, center_y + 40, input_width, input_height),
            'label': 'Puerto:',
            'name': 'port',
            'color': (200, 200, 200),
            'active_color': (255, 255, 255),
            'text_color': (0, 0, 0)
        }
        
        # Botones de acción
        action_button_width = 180
        action_button_height = 50
        
        self.connect_button = {
            'rect': pygame.Rect(center_x - action_button_width - 10, center_y + 120, action_button_width, action_button_height),
            'text': 'Conectar',
            'color': (34, 139, 34),
            'hover_color': (50, 205, 50)
        }
        
        self.cancel_button = {
            'rect': pygame.Rect(center_x + 10, center_y + 120, action_button_width, action_button_height),
            'text': 'Cancelar',
            'color': (180, 70, 70),
            'hover_color': (220, 100, 100)
        }
    
    def handle_event(self, event):
        """Manejar eventos del diálogo"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Click en modo LAN
            if self.lan_button['rect'].collidepoint(mouse_pos):
                self.connection_mode = 'lan'
                self.host_input = 'localhost'
                self.port_input = '8888'
            
            # Click en modo Online
            elif self.online_button['rect'].collidepoint(mouse_pos):
                self.connection_mode = 'online'
                self.host_input = '0.tcp.ngrok.io'
                self.port_input = '12345'
            
            # Click en campo de host
            elif self.host_field['rect'].collidepoint(mouse_pos):
                self.active_input = 'host'
            
            # Click en campo de puerto
            elif self.port_field['rect'].collidepoint(mouse_pos):
                self.active_input = 'port'
            
            # Click en botón conectar
            elif self.connect_button['rect'].collidepoint(mouse_pos):
                self.result = {
                    'mode': self.connection_mode,
                    'host': self.host_input,
                    'port': int(self.port_input) if self.port_input.isdigit() else 8888
                }
                self.active = False
            
            # Click en botón cancelar
            elif self.cancel_button['rect'].collidepoint(mouse_pos):
                self.result = None
                self.active = False
        
        elif event.type == pygame.KEYDOWN:
            if self.active_input == 'host':
                if event.key == pygame.K_BACKSPACE:
                    self.host_input = self.host_input[:-1]
                elif event.key == pygame.K_TAB:
                    self.active_input = 'port'
                elif event.key == pygame.K_RETURN:
                    self.result = {
                        'mode': self.connection_mode,
                        'host': self.host_input,
                        'port': int(self.port_input) if self.port_input.isdigit() else 8888
                    }
                    self.active = False
                elif event.unicode and len(self.host_input) < 50:
                    self.host_input += event.unicode
            
            elif self.active_input == 'port':
                if event.key == pygame.K_BACKSPACE:
                    self.port_input = self.port_input[:-1]
                elif event.key == pygame.K_TAB:
                    self.active_input = 'host'
                elif event.key == pygame.K_RETURN:
                    self.result = {
                        'mode': self.connection_mode,
                        'host': self.host_input,
                        'port': int(self.port_input) if self.port_input.isdigit() else 8888
                    }
                    self.active = False
                elif event.unicode.isdigit() and len(self.port_input) < 5:
                    self.port_input += event.unicode
    
    def draw(self):
        """Dibujar el diálogo"""
        # Fondo semi-transparente
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 40))
        self.screen.blit(overlay, (0, 0))
        
        # Título
        title = self.font_title.render("Configuración de Conexión", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width//2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_small.render("Selecciona el modo de conexión:", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.width//2, 150))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Dibujar botones de modo
        mouse_pos = pygame.mouse.get_pos()
        
        for button in [self.lan_button, self.online_button]:
            # Determinar color
            if self.connection_mode == button['mode']:
                color = button['selected_color']
            elif button['rect'].collidepoint(mouse_pos):
                color = button['hover_color']
            else:
                color = button['color']
            
            # Dibujar botón
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=5)
            pygame.draw.rect(self.screen, (255, 255, 255), button['rect'], 2, border_radius=5)
            
            # Texto
            text = self.font_normal.render(button['text'], True, (255, 255, 255))
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
        
        # Información del modo seleccionado
        if self.connection_mode == 'lan':
            info_text = "Conectar a servidor local o en la misma red (LAN)"
            info_color = (150, 200, 255)
        else:
            info_text = "Conectar a servidor remoto usando ngrok (requiere URL de ngrok)"
            info_color = (255, 200, 150)
        
        info = self.font_small.render(info_text, True, info_color)
        info_rect = info.get_rect(center=(self.width//2, 250))
        self.screen.blit(info, info_rect)
        
        # Dibujar campos de entrada
        for field in [self.host_field, self.port_field]:
            # Color del campo
            if self.active_input == field['name']:
                color = field['active_color']
                border_color = (100, 200, 255)
            else:
                color = field['color']
                border_color = (255, 255, 255)
            
            # Dibujar campo
            pygame.draw.rect(self.screen, color, field['rect'], border_radius=3)
            pygame.draw.rect(self.screen, border_color, field['rect'], 2, border_radius=3)
            
            # Label
            label = self.font_small.render(field['label'], True, (200, 200, 200))
            label_rect = label.get_rect(midright=(field['rect'].left - 10, field['rect'].centery))
            self.screen.blit(label, label_rect)
            
            # Texto del campo
            text_value = self.host_input if field['name'] == 'host' else self.port_input
            text = self.font_normal.render(text_value, True, field['text_color'])
            text_rect = text.get_rect(midleft=(field['rect'].left + 10, field['rect'].centery))
            self.screen.blit(text, text_rect)
            
            # Cursor parpadeante si está activo
            if self.active_input == field['name']:
                cursor_x = text_rect.right + 2
                cursor_y1 = field['rect'].centery - 15
                cursor_y2 = field['rect'].centery + 15
                if int(pygame.time.get_ticks() / 500) % 2:
                    pygame.draw.line(self.screen, (0, 0, 0), (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)
        
        # Dibujar botones de acción
        for button in [self.connect_button, self.cancel_button]:
            # Color
            if button['rect'].collidepoint(mouse_pos):
                color = button['hover_color']
            else:
                color = button['color']
            
            # Dibujar
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=5)
            pygame.draw.rect(self.screen, (255, 255, 255), button['rect'], 2, border_radius=5)
            
            # Texto
            text = self.font_normal.render(button['text'], True, (255, 255, 255))
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
        
        # Ayuda en la parte inferior
        help_texts = [
            "💡 LAN: Para jugar en la misma red WiFi (usa localhost o IP local)",
            "🌐 Online: Para jugar desde cualquier lugar (necesitas la URL de ngrok del servidor)"
        ]
        
        y_offset = self.height - 120
        for help_text in help_texts:
            help_surface = self.font_small.render(help_text, True, (150, 150, 150))
            help_rect = help_surface.get_rect(center=(self.width//2, y_offset))
            self.screen.blit(help_surface, help_rect)
            y_offset += 30
    
    def run(self):
        """Ejecutar el diálogo y retornar el resultado"""
        clock = pygame.time.Clock()
        
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return self.result
