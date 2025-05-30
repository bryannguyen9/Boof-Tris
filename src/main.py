import pygame
from pygame import init, display, event, QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE, VIDEORESIZE, mixer
import random
import game_logic
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, GRID_ROWS, GRID_COLS,
                    MENU_MUSIC, GAME_MUSIC,
                    STATE_MENU, STATE_PLAYING, STATE_GAMEOVER, STATE_SAVE, STATE_LEADERBOARD, JEWEL_COLORS)
from ui import draw_menu, draw_grid, draw_gameover, draw_save_screen, draw_leaderboard
from utils import calculate_cell_size
import leaderboard

def main():
    init()
    mixer.init()
    # Start with menu music
    mixer.music.load(MENU_MUSIC)
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)

    screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    display.set_caption("BOOF-TRIS")
    clock = pygame.time.Clock()

    state = STATE_MENU
    prev_state = None
    game = None
    buttons = {}
    timers = {'faller': 0, 'highlight': None}
    speeds = {'faller': 200, 'highlight': 500}

    running = True
    while running:
        elapsed = clock.tick(60)
        for e in event.get():
            if e.type == QUIT:
                running = False

            # Menu interactions
            if state == STATE_MENU and e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos
                if buttons.get('start').collidepoint((x, y)):
                    state = STATE_PLAYING
                    game = game_logic.Game(GRID_ROWS, GRID_COLS)
                    timers = {'faller': 0, 'highlight': None}
                elif buttons.get('leader').collidepoint((x, y)):
                    state = STATE_LEADERBOARD

            # Playing interactions
            elif state == STATE_PLAYING:
                if e.type == KEYDOWN:
                    if e.key == K_LEFT:  game.move_faller_left()
                    elif e.key == K_RIGHT: game.move_faller_right()
                    elif e.key == K_SPACE: game.rotate_faller()
                elif e.type == VIDEORESIZE:
                    display.set_mode((e.w, e.h), pygame.RESIZABLE)

            # Game over interactions
            elif state == STATE_GAMEOVER and e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos
                if buttons.get('play').collidepoint((x, y)):
                    state = STATE_PLAYING
                    game = game_logic.Game(GRID_ROWS, GRID_COLS)
                    timers = {'faller': 0, 'highlight': None}
                elif buttons.get('menu').collidepoint((x, y)):
                    state = STATE_MENU
                elif buttons['save'].collidepoint((x, y)):
                    state = STATE_SAVE
                    name_text = ""
                    error_msg = None
            
            # save score
            elif state == STATE_SAVE and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    name_text = name_text[:-1]
                elif e.key == pygame.K_RETURN:
                    if 1 <= len(name_text) <= 10:
                        leaderboard.add_score(name_text, game.score)
                        state = STATE_LEADERBOARD
                    else:
                        error_msg = "Must be 1–10 chars"
                else:
                    if len(name_text) < 10 and e.unicode.isalnum():
                        name_text += e.unicode

            # Leaderboard back button
            elif state == STATE_LEADERBOARD and e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos
                if buttons['back'].collidepoint((x, y)):
                    state = STATE_MENU

        # Detect state changes
        if state != prev_state:
            if state == STATE_MENU:
                mixer.music.load(MENU_MUSIC)
                mixer.music.play(-1)
            elif state == STATE_PLAYING:
                mixer.music.load(GAME_MUSIC)
                mixer.music.play(-1)
            elif state == STATE_GAMEOVER:
                mixer.music.stop()
            prev_state = state

        # State-specific draws & logic
        if state == STATE_MENU:
            buttons['start'], buttons['leader'] = draw_menu(screen)

        elif state == STATE_PLAYING:
            if game.game_over:
                state = STATE_GAMEOVER
                continue

            # Highlight phase
            if game.highlighting_matches:
                if timers['highlight'] is None:
                    timers['highlight'] = pygame.time.get_ticks()
                if pygame.time.get_ticks() - timers['highlight'] >= speeds['highlight']:
                    game.clear_marked_matches()
                    timers['highlight'] = None
                else:
                    size = calculate_cell_size(*screen.get_size(), GRID_ROWS, GRID_COLS)
                    draw_grid(screen, game.grid, size, game.score)
                    continue

            # Regular update
            timers['faller'] += elapsed
            if timers['faller'] >= speeds['faller']:
                game.update()
                timers['faller'] = 0

            if not game.faller:
                cols = [c for c in range(GRID_COLS) if game.grid[0][c] == ' ']
                if cols:
                    c = random.choice(cols)
                    js = random.choices(list(JEWEL_COLORS.keys())[:-1], k=3)
                    game.spawn_faller(c + 1, js)
                else:
                    state = STATE_GAMEOVER
                    continue

            size = calculate_cell_size(*screen.get_size(), GRID_ROWS, GRID_COLS)
            draw_grid(screen, game.grid, size, game.score)

        elif state == STATE_GAMEOVER:
            buttons['play'], buttons['menu'], buttons['save'] = draw_gameover(screen)
            
        elif state == STATE_SAVE:
            draw_save_screen(screen, game.score, name_text, error_msg)
        
        elif state == STATE_LEADERBOARD:
            buttons['back'] = draw_leaderboard(screen, leaderboard.get_entries())

    pygame.quit()

if __name__ == "__main__":
    main()