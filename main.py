import pygame
import time
from camera import Camera
from game_ui import draw_login_screen, draw_game_ui
from leaderboard import save_leaderboard, show_leaderboard

WIDTH, HEIGHT = 1100, 700
SCOREBOARD_TOTAL = 10
TIMER_SECONDS = 20


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Tello Logistik')

    player_name = draw_login_screen(screen)
    camera = Camera()
    clock = pygame.time.Clock()
    start_time = time.time()
    timer_done = False
    final_score = 0

    running = True
    while running:
        elapsed = int(time.time() - start_time)
        time_left = max(0, TIMER_SECONDS - elapsed)
        if time_left == 0 and not timer_done:
            timer_done = True
            final_score = min(len(camera.detections), SCOREBOARD_TOTAL)
            save_leaderboard(player_name, final_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        frame, current_detection = (None, '')
        if not timer_done:
            frame, current_detection = camera.get_frame_and_detect()

        draw_game_ui(
            screen,
            frame,
            current_detection,
            camera.detections,
            time_left,
            timer_done,
            final_score,
            SCOREBOARD_TOTAL
        )

        if timer_done:
            show_leaderboard(screen)
            running = False

        pygame.display.flip()
        clock.tick(30)

    camera.release()
    pygame.quit()

if __name__ == '__main__':
    main()
