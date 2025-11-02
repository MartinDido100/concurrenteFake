"""
Diálogo de configuración de conexión para el juego Batalla Naval
Permite introducir la dirección del servidor
"""

import pygame
import sys
import os

class ConnectionDialog:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Estado del diálogo
        self.active = True
        self.result = None  # {'host': str, 'port': int}
        
        # Campos de texto - Vacíos por defecto
        self.host_input = ''
        self.port_input = ''
        self.active_input = 'host'  # 'host' o 'port'
        
        # Imagen de fondo del menú
        self.menu_image = None
        self.load_menu_background()
        
        # Fuentes
        self.font_title = pygame.font.Font(None, 48)
        self.font_normal = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Configurar elementos de UI
        self.setup_ui()
    
    def load_menu_background(self):
        """Cargar la imagen de fondo del menú"""
        try:
            self.menu_image = pygame.image.load('assets/images/menu.png')
            self.menu_image = pygame.transform.scale(self.menu_image, (self.width, self.height))
        except pygame.error:
            self.menu_image = None
    
    def draw_menu_background(self):
        """Dibujar el mismo fondo que el menú principal"""
        if self.menu_image:
            self.screen.blit(self.menu_image, (0, 0))
        else:
            self.screen.fill((30, 30, 60))
        
    def setup_ui(self):
        """Configurar elementos de la interfaz"""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Campos de entrada
        input_width = 450
        input_height = 55
        
        self.host_field = {
            'rect': pygame.Rect(center_x - input_width//2, center_y - 80, input_width, input_height),
            'label': 'Host / IP:',
            'name': 'host',
            'color': (200, 200, 200),
            'active_color': (255, 255, 255),
            'text_color': (0, 0, 0)
        }
        
        self.port_field = {
            'rect': pygame.Rect(center_x - input_width//2, center_y + 10, input_width, input_height),
            'label': 'Puerto:',
            'name': 'port',
            'color': (200, 200, 200),
            'active_color': (255, 255, 255),
            'text_color': (0, 0, 0)
        }
        
        # Botones de acción
        action_button_width = 200
        action_button_height = 55
        
        self.connect_button = {
            'rect': pygame.Rect(center_x - action_button_width - 10, center_y + 100, action_button_width, action_button_height),
            'text': 'Conectar',
            'color': (34, 139, 34),
            'hover_color': (50, 205, 50)
        }
        
        self.cancel_button = {
            'rect': pygame.Rect(center_x + 10, center_y + 100, action_button_width, action_button_height),
            'text': 'Cancelar',
            'color': (180, 70, 70),
            'hover_color': (220, 100, 100)
        }
    
    def handle_event(self, event):
        """Manejar eventos del diálogo"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Click en campo de host
            if self.host_field['rect'].collidepoint(mouse_pos):
                self.active_input = 'host'
            
            # Click en campo de puerto
            elif self.port_field['rect'].collidepoint(mouse_pos):
                self.active_input = 'port'
            
            # Click en botón conectar
            elif self.connect_button['rect'].collidepoint(mouse_pos):
                # Validar que los campos no estén vacíos
                if not self.host_input.strip():
                    print("⚠️ Debes ingresar el Host/IP")
                    return
                
                if not self.port_input.strip() or not self.port_input.isdigit():
                    print("⚠️ Debes ingresar un puerto válido")
                    return
                
                # Todo válido, crear resultado
                self.result = {
                    'host': self.host_input.strip(),
                    'port': int(self.port_input)
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
                    # Validar antes de conectar
                    if not self.host_input.strip():
                        print("⚠️ Debes ingresar el Host/IP")
                    elif not self.port_input.strip() or not self.port_input.isdigit():
                        print("⚠️ Debes ingresar un puerto válido")
                    else:
                        self.result = {
                            'host': self.host_input.strip(),
                            'port': int(self.port_input)
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
                    # Validar antes de conectar
                    if not self.host_input.strip():
                        print("⚠️ Debes ingresar el Host/IP")
                    elif not self.port_input.strip() or not self.port_input.isdigit():
                        print("⚠️ Debes ingresar un puerto válido")
                    else:
                        self.result = {
                            'host': self.host_input.strip(),
                            'port': int(self.port_input)
                        }
                        self.active = False
                elif event.unicode.isdigit() and len(self.port_input) < 5:
                    self.port_input += event.unicode
    
    def draw(self):
        """Dibujar el diálogo"""
        # Fondo igual que el del menú principal
        self.draw_menu_background()
        
        # Overlay semi-transparente para oscurecer un poco
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 20))
        self.screen.blit(overlay, (0, 0))
        
        # Título
        title = self.font_title.render("Conectar al Servidor", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width//2, 120))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_small.render("Ingresa la dirección del servidor ngrok:", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.width//2, 170))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Obtener posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        
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
            
            # Texto del campo o placeholder
            text_value = self.host_input if field['name'] == 'host' else self.port_input
            
            # Si está vacío, mostrar placeholder
            if not text_value:
                if field['name'] == 'host':
                    placeholder = "Ejemplo: 0.tcp.ngrok.io"
                    placeholder_color = (120, 120, 120)
                else:  # port
                    placeholder = "Ejemplo: 12345"
                    placeholder_color = (120, 120, 120)
                
                text = self.font_normal.render(placeholder, True, placeholder_color)
                text_rect = text.get_rect(midleft=(field['rect'].left + 10, field['rect'].centery))
                self.screen.blit(text, text_rect)
            else:
                # Mostrar texto ingresado
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
