"""
Pantalla de fin de juego para Batalla Naval
Muestra el resultado de la partida
"""

import pygame
import sys
import os

# Importar constants desde la carpeta padre del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
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