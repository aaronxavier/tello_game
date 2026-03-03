import yaml
import os
import pygame

CONFIG_FILE = 'leaderboard.yaml'

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

def reset_leaderboard():
    """Reset the leaderboard by removing the config file."""
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print(f"Leaderboard has been reset.")

def show_leaderboard(screen):
    if not os.path.exists(CONFIG_FILE):
        return False
    with open(CONFIG_FILE, 'r') as f:
        try:
            data = yaml.safe_load(f) or {}
        except Exception:
            data = {}
    sorted_scores = sorted(data.items(), key=lambda x: x[1], reverse=True)
    font_big = pygame.font.SysFont('Arial', 36)
    
    running = True
    play_again = False
    
    while running:
        width, height = screen.get_width(), screen.get_height()
        screen.fill(FLW_GRAY)
        
        # Draw leaderboard title and entries
        title = font_big.render('Leaderboard', True, FLW_DARK_GREEN)
        title_y = 80
        screen.blit(title, (width // 2 - title.get_width() // 2, title_y))
        
        # Center the entries as a block
        entry_height = 40
        start_y = title_y + title.get_height() + 20
        for i, (name, score) in enumerate(sorted_scores):
            entry = f"{i+1}. {name}: {score}"
            entry_surf = font.render(entry, True, FLW_ACCENT if i == 0 else FLW_GREEN)
            screen.blit(entry_surf, (width // 2 - entry_surf.get_width() // 2, start_y + i * entry_height))
        
        # Draw "Start Again" button
        start_again_button = pygame.Rect(width // 2 - 250, height - 120, 200, 50)
        pygame.draw.rect(screen, FLW_GREEN, start_again_button, border_radius=10)
        start_text = font.render('Start Again', True, WHITE)
        screen.blit(start_text, (start_again_button.x + (start_again_button.width - start_text.get_width()) // 2,
                                  start_again_button.y + (start_again_button.height - start_text.get_height()) // 2))
        
        # Draw "Exit" button
        exit_button = pygame.Rect(width // 2 + 50, height - 120, 200, 50)
        pygame.draw.rect(screen, FLW_ACCENT, exit_button, border_radius=10)
        exit_text = font.render('Exit', True, BLACK)
        screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2,
                                 exit_button.y + (exit_button.height - exit_text.get_height()) // 2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                play_again = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                play_again = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_again_button.collidepoint(event.pos):
                    running = False
                    play_again = True
                elif exit_button.collidepoint(event.pos):
                    running = False
                    play_again = False
    
    return play_again
