import sys
import argparse
import pygame
import time
from camera import Camera
from game_ui import draw_login_screen, draw_game_ui
from game_ui_vr import draw_game_ui_vr
from leaderboard import save_leaderboard, show_leaderboard, reset_leaderboard

WIDTH, HEIGHT = 1100, 700
SCOREBOARD_TOTAL = 20
TIMER_SECONDS = 12

# Colors (FLW theme)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FLW_GREEN = (153, 199, 48)  # #99C730
FLW_DARK_GREEN = (120, 162, 44)  # Approximate for contrast
FLW_GRAY = (245, 245, 245)  # Light background
FLW_ACCENT = (170, 204, 0)  # #AACC00 (for highlights)


def parse_args():
    parser = argparse.ArgumentParser(description='Tello Logistik')
    parser.add_argument('--use-device', type=int, default=0, help='Camera device ID (default: 0)')
    parser.add_argument('--use-topic', type=str, nargs='?', const='/image_raw', default=None, help='Read images from ROS topic (default: /image_raw)')
    parser.add_argument('--reset-leaderboard', action='store_true', help='Reset the leaderboard and exit')
    return parser.parse_args()


def main():
    args = parse_args()
    
    # Handle reset leaderboard flag
    if args.reset_leaderboard:
        reset_leaderboard()
        return
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Tello Logistik')

    # Create camera once and reuse it across game restarts
    if args.use_topic:
        camera = Camera(use_topic=True, topic=args.use_topic)
    else:
        camera = Camera(device=args.use_device)

    play_again = True
    while play_again:
        # Reset camera detections for new game
        camera.reset()
        
        player_name, vr_mode = draw_login_screen(screen)
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

            frame, current_detection = (None, '')
            if not timer_done:
                frame, current_detection = camera.get_frame_and_detect()

            if vr_mode:
                draw_game_ui_vr(
                    screen,
                    frame,
                    current_detection,
                    camera.detections,
                    time_left,
                    timer_done,
                    final_score,
                    SCOREBOARD_TOTAL
                )
            else:
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
                pygame.display.flip()
                pygame.time.wait(2000)
                play_again = show_leaderboard(screen)
                running = False
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    play_again = False

            pygame.display.flip()
            clock.tick(30)

    # Clean up camera only once when exiting
    camera.release()
    pygame.quit()


if __name__ == '__main__':
    main()
