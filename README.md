# Tello Logistik Game

This project is a QR code detection game using Pygame and OpenCV, with optional ROS2 camera integration and a persistent YAML-based leaderboard.

## Features
- Detects QR codes from a webcam or a ROS2 image topic (`/camera/image_raw`).
- Game UI with timer, score, and detection list.
- Player login screen.
- Leaderboard saved in `leaderboard.yaml`.
- Detections saved in `detections.yaml`.

## Requirements
- Python 3.10+
- OpenCV (`opencv-python`)
- Pygame
- PyYAML
- (Optional, for ROS2 integration):
  - ROS2 Humble or newer
  - `rclpy`, `cv_bridge`, `sensor_msgs`

## Installation
```bash
pip install -r requirements.txt
# For ROS2 integration, ensure your ROS2 environment is sourced and dependencies installed
```

## Usage

### Run with Webcam (default)
```bash
python3 main.py
```

### Run with ROS2 Image Topic
```bash
python3 main.py --use-topic
```

- On start, enter your player name.
- The game runs for 20 seconds (default, configurable in `main.py`).
- Scan as many unique QR codes as possible.
- Your score and name are saved to `leaderboard.yaml`.
- The leaderboard is displayed after each game.

## File Structure
- `main.py` - Main entry point, handles game loop and CLI args.
- `camera.py` - Camera and QR detection logic (webcam or ROS2 topic).
- `game_ui.py` - Pygame UI drawing functions.
- `leaderboard.py` - Leaderboard save/display logic.
- `detections.yaml` - Stores detected QR codes for the current game.
- `leaderboard.yaml` - Stores all player scores.

## Notes
- To use ROS2, source your ROS2 environment before running the game.
