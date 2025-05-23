import yaml
import os
import pygame

CONFIG_FILE = 'leaderboard.yaml'
LOGO_PATH = 'images/logo.png'

# FLW color theme
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FLW_GREEN = (153, 199, 48)  # #99C730
FLW_DARK_GREEN = (120, 162, 44)
FLW_GRAY = (245, 245, 245)
FLW_ACCENT = (170, 204, 0)  # #AACC00
WIDTH, HEIGHT = 1100, 700

pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

def save_leaderboard(name, score):
    data = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            try:
                data = yaml.safe_load(f) or {}
            except Exception:
                data = {}
    data[name] = score
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(data, f)

def show_leaderboard(screen):
    if not os.path.exists(CONFIG_FILE):
        return
    with open(CONFIG_FILE, 'r') as f:
        try:
            data = yaml.safe_load(f) or {}
        except Exception:
            data = {}
    sorted_scores = sorted(data.items(), key=lambda x: x[1], reverse=True)
    font_big = pygame.font.SysFont('Arial', 36)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        screen.fill(FLW_GRAY)
        title = font_big.render('Leaderboard', True, FLW_DARK_GREEN)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        for i, (name, score) in enumerate(sorted_scores):
            entry = f"{i+1}. {name}: {score}"
            entry_surf = font.render(entry, True, FLW_ACCENT if i == 0 else FLW_GREEN)
            screen.blit(entry_surf, (WIDTH // 2 - 150, 150 + i * 40))
        info = small_font.render('Press ESC to exit', True, FLW_DARK_GREEN)
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT - 60))
        pygame.display.flip()
