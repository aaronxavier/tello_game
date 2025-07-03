import pygame
import numpy as np
import os

WIDTH, HEIGHT = 1100, 700
FRAME_W, FRAME_H = 640, 480
SIDE_BOX_W = 200
SPACING = 10

# Colors (FLW theme)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FLW_GREEN = (153, 199, 48)  # #99C730
FLW_DARK_GREEN = (120, 162, 44)  # Approximate for contrast
FLW_GRAY = (245, 245, 245)  # Light background
FLW_ACCENT = (170, 204, 0)  # #AACC00 (for highlights)

pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)
LOGO_PATH = 'images/logo.png'


def draw_login_screen(screen):
    width, height = screen.get_width(), screen.get_height()
    input_box = pygame.Rect(width // 2 - 150, height // 2 - 32, 300, 48)
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
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                width, height = event.w, event.h
                input_box = pygame.Rect(width // 2 - 150, height // 2 - 32, 300, 48)
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
        screen.fill(FLW_GRAY)
        title = font_big.render('Enter Player Name', True, FLW_DARK_GREEN)
        screen.blit(title, (width // 2 - title.get_width() // 2, height // 2 - 100))
        pygame.draw.rect(screen, FLW_GREEN if active else FLW_ACCENT, input_box, 2)
        txt_surface = font.render(text, True, BLACK)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        # Draw logo at bottom center
        if os.path.exists(LOGO_PATH):
            logo_img = pygame.image.load(LOGO_PATH)
            logo_rect = logo_img.get_rect()
            # Scale logo to 1/3 of its original size
            logo_img = pygame.transform.smoothscale(logo_img, (logo_rect.width // 3, logo_rect.height // 3))
            logo_rect = logo_img.get_rect()
            logo_rect.midbottom = (width // 2, height - 10)
            screen.blit(logo_img, logo_rect)
        pygame.display.flip()
    return text.strip()


def draw_game_ui(screen, frame, current_detection, detections, time_left, timer_done, final_score, scoreboard_total):
    width, height = screen.get_width(), screen.get_height()
    frame_w, frame_h = min(640, width - 300), min(480, height - 200)
    side_box_w = 200
    spacing = 10
    # Draw background
    screen.fill(FLW_GRAY)
    # Draw timer at top middle
    timer_color = (255, 0, 0) if time_left <= 10 else FLW_DARK_GREEN
    timer_text = f"Time Left: {time_left:02d}s"
    timer_surf = font.render(timer_text, True, timer_color)
    timer_rect = timer_surf.get_rect(center=(width // 2, 20))
    screen.blit(timer_surf, timer_rect)
    if not timer_done:
        # Draw frame in center-left
        frame_x = (width - frame_w - side_box_w - spacing) // 2
        frame_y = 50
        frame_rgb = None
        frame_surface = None
        if frame is not None:
            frame_rgb = np.rot90(frame)
            frame_surface = pygame.surfarray.make_surface(frame_rgb)
            frame_surface = pygame.transform.scale(frame_surface, (frame_w, frame_h))
            frame_surface = pygame.transform.flip(frame_surface, True, False)
            screen.blit(frame_surface, (frame_x, frame_y))
        # Draw current detection under frame
        detect_text = f"Current Detection: {current_detection if current_detection else 'None'}"
        detect_surf = font.render(detect_text, True, FLW_DARK_GREEN)
        screen.blit(detect_surf, (frame_x, frame_y + frame_h + 20))
        # Draw detections box on right with 10pt space
        box_x = frame_x + frame_w + spacing
        box_y = 50
        box_h = height - 100
        pygame.draw.rect(screen, FLW_GREEN, (box_x, box_y, side_box_w, box_h), border_radius=10)
        title_surf = font.render('Detections', True, WHITE)
        screen.blit(title_surf, (box_x + 20, box_y + 10))
        # Draw scoreboard at top right of detections box
        score_text = f"Score: {min(len(detections), scoreboard_total)}/{scoreboard_total}"
        score_surf = font.render(score_text, True, FLW_ACCENT)
        screen.blit(score_surf, (box_x + 20, box_y - 35))
        # List detections
        for i, d in enumerate(sorted(detections)):
            det_surf = small_font.render(d, True, WHITE)
            screen.blit(det_surf, (box_x + 20, box_y + 50 + i * 30))
    else:
        final_text = f"Time's up! Final Score: {final_score}/{scoreboard_total}"
        final_surf = font.render(final_text, True, (200, 0, 0))
        final_rect = final_surf.get_rect(center=(width // 2, height // 2 - 40))
        screen.blit(final_surf, final_rect)
        pygame.display.flip()
        pygame.time.wait(2000)