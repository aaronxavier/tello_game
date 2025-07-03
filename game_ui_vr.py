import pygame
import numpy as np
import os

# Colors (FLW theme)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FLW_GREEN = (153, 199, 48)
FLW_DARK_GREEN = (120, 162, 44)
FLW_GRAY = (245, 245, 245)
FLW_ACCENT = (170, 204, 0)

pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)
LOGO_PATH = 'images/logo.png'


def draw_login_screen_vr(screen):
    width, height = screen.get_width(), screen.get_height()
    input_box = pygame.Rect(width // 2 - 150, height // 2 - 32, 300, 48)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    font_big = pygame.font.SysFont('Arial', 36)
    vr_mode = False
    vr_toggle_rect = pygame.Rect(width - 170, 20, 150, 40)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                width, height = event.w, event.h
                input_box = pygame.Rect(width // 2 - 150, height // 2 - 32, 300, 48)
                vr_toggle_rect = pygame.Rect(width - 170, 20, 150, 40)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if vr_toggle_rect.collidepoint(event.pos):
                    vr_mode = not vr_mode
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
        # VR toggle
        pygame.draw.rect(screen, FLW_ACCENT if vr_mode else FLW_GRAY, vr_toggle_rect, border_radius=10)
        vr_label = font.render('VR Mode', True, BLACK)
        check = font.render('✔' if vr_mode else '', True, FLW_GREEN)
        screen.blit(vr_label, (vr_toggle_rect.x + 10, vr_toggle_rect.y + 7))
        screen.blit(check, (vr_toggle_rect.x + 110, vr_toggle_rect.y + 7))
        # Draw logo at bottom center
        if os.path.exists(LOGO_PATH):
            logo_img = pygame.image.load(LOGO_PATH)
            logo_rect = logo_img.get_rect()
            logo_img = pygame.transform.smoothscale(logo_img, (logo_rect.width // 3, logo_rect.height // 3))
            logo_rect = logo_img.get_rect()
            logo_rect.midbottom = (width // 2, height - 10)
            screen.blit(logo_img, logo_rect)
        pygame.display.flip()
    return text.strip(), vr_mode


def draw_game_ui_vr(screen, frame, current_detection, detections, time_left, timer_done, final_score, scoreboard_total):
    width, height = screen.get_width(), screen.get_height()
    # Draw video as full background
    if frame is not None:
        frame_rgb = np.rot90(frame)
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        frame_surface = pygame.transform.scale(frame_surface, (width, height))
        frame_surface = pygame.transform.flip(frame_surface, True, False)
        screen.blit(frame_surface, (0, 0))
    else:
        screen.fill(BLACK)
    # Floating timer (top center)
    timer_color = (255, 0, 0) if time_left <= 10 else FLW_DARK_GREEN
    timer_text = f"Time Left: {time_left:02d}s"
    timer_surf = font.render(timer_text, True, timer_color)
    timer_rect = timer_surf.get_rect(center=(width // 2, 40))
    pygame.draw.rect(screen, FLW_GRAY, timer_rect.inflate(30, 20), border_radius=10)
    screen.blit(timer_surf, timer_rect)
    # Floating detections (right middle)
    box_w, box_h = 220, 40 + 30 * min(6, len(detections))
    box_x = width - box_w - 40
    box_y = height // 2 - box_h // 2
    pygame.draw.rect(screen, FLW_GREEN, (box_x, box_y, box_w, box_h), border_radius=10)
    title_surf = font.render('Detections', True, WHITE)
    screen.blit(title_surf, (box_x + 20, box_y + 10))
    for i, d in enumerate(sorted(detections)[:6]):
        det_surf = small_font.render(d, True, WHITE)
        screen.blit(det_surf, (box_x + 20, box_y + 50 + i * 30))
    # Floating score (top right)
    score_text = f"Score: {min(len(detections), scoreboard_total)}/{scoreboard_total}"
    score_surf = font.render(score_text, True, FLW_ACCENT)
    score_rect = score_surf.get_rect(topright=(width - 40, 20))
    pygame.draw.rect(screen, FLW_GRAY, score_rect.inflate(30, 20), border_radius=10)
    screen.blit(score_surf, score_rect)
    # Floating current detection (bottom center)
    detect_text = f"Current Detection: {current_detection if current_detection else 'None'}"
    detect_surf = font.render(detect_text, True, FLW_DARK_GREEN)
    detect_rect = detect_surf.get_rect(center=(width // 2, height - 40))
    pygame.draw.rect(screen, FLW_GRAY, detect_rect.inflate(30, 20), border_radius=10)
    screen.blit(detect_surf, detect_rect)
    # Final score overlay if timer done
    if timer_done:
        final_text = f"Time's up! Final Score: {final_score}/{scoreboard_total}"
        final_surf = font.render(final_text, True, (200, 0, 0))
        final_rect = final_surf.get_rect(center=(width // 2, height // 2 - 40))
        pygame.draw.rect(screen, FLW_GRAY, final_rect.inflate(40, 30), border_radius=10)
        screen.blit(final_surf, final_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
