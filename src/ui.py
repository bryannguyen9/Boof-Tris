import pygame
from config import BACKGROUND_COLOR, GRID_COLOR, JEWEL_COLORS, WINDOW_WIDTH, WINDOW_HEIGHT
from utils import calculate_cell_size, draw_button

# Draw main menu, grid, gameover, save, leaderboard screens

def draw_menu(screen):
    screen.fill(BACKGROUND_COLOR)
    title = pygame.font.Font(None, 120).render("BOOF-TRIS", True, (255,255,255))
    screen.blit(title, title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3)))
    btn_font = pygame.font.Font(None, 36)
    start = pygame.Rect(WINDOW_WIDTH//2-100, 400, 200, 60)
    leader = pygame.Rect(WINDOW_WIDTH//2-100, 480, 200, 60)
    draw_button(screen, start, "Start Game", btn_font, (50,150,50))
    draw_button(screen, leader, "Leaderboard", btn_font, (50,50,150))
    pygame.display.flip()
    return start, leader


def draw_grid(screen, grid, cell_size, score):
    screen.fill(BACKGROUND_COLOR)
    highlight = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    for r,row in enumerate(grid):
        for c,cell in enumerate(row):
            val = cell.strip('[]|* ')
            color = JEWEL_COLORS.get(val, BACKGROUND_COLOR)
            rect = pygame.Rect(c*cell_size, r*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            if cell.startswith("|") or cell.startswith("("):
                highlight.fill((255,255,255,128)); screen.blit(highlight, rect.topleft)
            elif cell.startswith("*"):
                highlight.fill((255,0,0,128)); screen.blit(highlight, rect.topleft)
    # score stacked
    font = pygame.font.Font(None, 36)
    lbl = font.render("SCORE", True, (255,255,255))
    val = font.render(str(score), True, (255,255,255))
    max_w = max(lbl.get_width(), val.get_width())
    x = screen.get_width() - max_w - 20
    y = 20
    screen.blit(lbl, (x,y))
    screen.blit(val, (x, y + lbl.get_height() + 5))
    pygame.display.flip()


def draw_gameover(screen):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,180)); screen.blit(overlay,(0,0))
    f = pygame.font.Font(None, 100)
    go = f.render("GAME OVER", True, (255,0,0))
    screen.blit(go, go.get_rect(center=(WINDOW_WIDTH//2, 200)))
    btn_font = pygame.font.Font(None, 36)
    play = pygame.Rect(WINDOW_WIDTH//2-100, 320, 200, 60)
    menu = pygame.Rect(WINDOW_WIDTH//2-100, 400, 200, 60)
    save = pygame.Rect(WINDOW_WIDTH//2-100, 480, 200, 60)
    draw_button(screen, play, "Play Again", btn_font, (50,150,50))
    draw_button(screen, menu, "Main Menu", btn_font, (150,50,50))
    draw_button(screen, save, "Save Score", btn_font, (50,50,200))
    pygame.display.flip()
    return play, menu, save


def draw_save_screen(screen, current_score, name_text, error):
    screen.fill(BACKGROUND_COLOR)
    f1 = pygame.font.Font(None, 48)
    f2 = pygame.font.Font(None, 36)
    prompt = f1.render("Enter name to save score:", True, (255,255,255))
    screen.blit(prompt, prompt.get_rect(center=(WINDOW_WIDTH//2, 200)))
    box = pygame.Rect(WINDOW_WIDTH//2-150, 260, 300, 50)
    pygame.draw.rect(screen, (255,255,255), box, 2)
    txt_surf = f2.render(name_text, True, (255,255,255))
    screen.blit(txt_surf, (box.x+10, box.y+10))
    score_lbl = f2.render(f"Score: {current_score}", True, (200,200,200))
    screen.blit(score_lbl, score_lbl.get_rect(center=(WINDOW_WIDTH//2, 330)))
    if error:
        err_s = f2.render(error, True, (255,50,50))
        screen.blit(err_s, (box.x, box.y+70))
    pygame.display.flip()


def draw_leaderboard(screen, entries):
    screen.fill(BACKGROUND_COLOR)
    f_title = pygame.font.Font(None, 72)
    header = f_title.render("Leaderboard", True, (255,255,255))
    screen.blit(header, header.get_rect(center=(WINDOW_WIDTH//2, 100)))
    f_entry = pygame.font.Font(None, 36)
    y = 180
    for name, score, date_str in entries:
        line = f_entry.render(f"{name}  {score}  {date_str}", True, (255,255,255))
        screen.blit(line, (WINDOW_WIDTH//2-100, y))
        y += 40
    # back button
    btn = pygame.Rect(WINDOW_WIDTH//2-100, y+20, 200, 50)
    draw_button(screen, btn, "Back", f_entry, (100,100,100))
    pygame.display.flip()
    return btn