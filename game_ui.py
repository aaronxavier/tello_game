import pygame
import numpy as np

WIDTH, HEIGHT = 1100, 700
FRAME_W, FRAME_H = 640, 480
SIDE_BOX_W = 200
SPACING = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
BLUE = (0, 120, 255)

pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)


def draw_login_screen(screen):
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 32, 300, 48)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    font_big = pygame.font.SysFont('Arial', 36)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text.strip():
                            done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 20:
                            text += event.unicode
        screen.fill(GRAY)
        title = font_big.render('Enter Player Name', True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(text, True, BLACK)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        pygame.display.flip()
    return text.strip()


def draw_game_ui(screen, frame, current_detection, detections, time_left, timer_done, final_score, scoreboard_total):
    # Draw background
    screen.fill(GRAY)
    # Draw timer at top middle
    timer_color = (255, 0, 0) if time_left <= 10 else BLACK
    timer_text = f"Time Left: {time_left:02d}s"
    timer_surf = font.render(timer_text, True, timer_color)
    timer_rect = timer_surf.get_rect(center=(WIDTH // 2, 20))
    screen.blit(timer_surf, timer_rect)
    if not timer_done:
        # Draw frame in center-left
        frame_x = (WIDTH - FRAME_W - SIDE_BOX_W - SPACING) // 2
        frame_y = 50
        frame_rgb = None
        frame_surface = None
        if frame is not None:
            frame_rgb = np.rot90(frame)
            frame_surface = pygame.surfarray.make_surface(frame_rgb)
            screen.blit(frame_surface, (frame_x, frame_y))
        # Draw current detection under frame
        detect_text = f"Current Detection: {current_detection if current_detection else 'None'}"
        detect_surf = font.render(detect_text, True, BLACK)
        screen.blit(detect_surf, (frame_x, frame_y + FRAME_H + 20))
        # Draw detections box on right with 10pt space
        box_x = frame_x + FRAME_W + SPACING
        box_y = 50
        pygame.draw.rect(screen, BLUE, (box_x, box_y, SIDE_BOX_W, HEIGHT - 100), border_radius=10)
        title_surf = font.render('Detections', True, WHITE)
        screen.blit(title_surf, (box_x + 20, box_y + 10))
        # Draw scoreboard at top right of detections box
        score_text = f"Score: {min(len(detections), scoreboard_total)}/{scoreboard_total}"
        score_surf = font.render(score_text, True, WHITE)
        screen.blit(score_surf, (box_x + 20, box_y - 35))
        # List detections
        for i, d in enumerate(sorted(detections)):
            det_surf = small_font.render(d, True, WHITE)
            screen.blit(det_surf, (box_x + 20, box_y + 50 + i * 30))
    else:
        # Timer done: show final score
        final_text = f"Time's up! Final Score: {final_score}/{scoreboard_total}"
        final_surf = font.render(final_text, True, (200, 0, 0))
        final_rect = final_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        screen.blit(final_surf, final_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
