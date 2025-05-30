import pygame
from config import BACKGROUND_COLOR

def calculate_cell_size(window_width, window_height, rows, cols):
    return min(window_width // cols, window_height // rows)


def draw_button(screen, rect, text, font, bg_color, fg_color=(255,255,255)):
    pygame.draw.rect(screen, bg_color, rect)
    txt_surf = font.render(text, True, fg_color)
    txt_rect = txt_surf.get_rect(center=rect.center)
    screen.blit(txt_surf, txt_rect)