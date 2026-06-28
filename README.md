# Tello Logistik Game

This project is a QR code detection game using Pygame and OpenCV, with optional ROS2 camera integration and a persistent YAML-based leaderboard.
![Splash](images/splash.png)

![GameUI](images/game_ui.png)

![Leaderboard](images/leaderboard.png)

## Features
- Detects QR codes from a webcam or a ROS2 image topic.
- **Two UI modes**: Standard and VR (immersive full-screen video with floating overlays).
- Game UI with timer, score, and detection list.
- Player login screen with VR mode toggle.
- Persistent leaderboard saved in `leaderboard.yaml`.
- **Start Again** option after viewing the leaderboard.
- Detections saved in `detections.yaml`.
- Command-line option to reset leaderboard.

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

### Running the Game

- Run with Webcam (default device 0)
    ```bash
    python3 main.py
    ```

-  Run with a specific webcam device (e.g., device 2)
    ```bash
    python3 main.py --use-device 2
    ```

- Run with ROS2 Image Topic (default: /image_raw)
    ```bash
    python3 main.py --use-topic
    ```

- Run with a specific ROS2 Image Topic
    ```bash
    python3 main.py --use-topic /camera/image_raw
    ```

- Reset the leaderboard
    ```bash
    python3 main.py --reset-leaderboard
    ```

### Playing the Game

1. **Login Screen**: Enter your player name and optionally toggle VR mode.
2. **Gameplay**: The game runs for 120 seconds. Scan as many unique QR codes as possible.
3. **Scoring**: Your final score (up to a maximum of 20 unique QR codes) is displayed.
4. **Leaderboard**: After the game ends, the leaderboard is automatically shown.
5. **Start Again**: Click "Start Again" to play another round, or "Exit" to quit.

### UI Modes

- **Standard Mode**: Side-by-side layout with video feed, detections panel, and timer.
- **VR Mode**: Immersive full-screen video background with floating UI elements overlaid on the video feed.

## File Structure
- `main.py` - Main entry point, handles game loop and CLI args.
- `camera.py` - Camera and QR detection logic (webcam or ROS2 topic).
- `game_ui.py`, `game_ui_vr.py` - Pygame UI drawing functions with immersive overlay.
- `leaderboard.py` - Leaderboard save/display logic with Start Again functionality.

## Configuration

You can modify game settings in `main.py`:

- `TIMER_SECONDS` - Game duration in seconds (default: 120)
- `SCOREBOARD_TOTAL` - Maximum number of unique QR codes counted toward score (default: 20)
- `WIDTH`, `HEIGHT` - Window dimensions (default: 1100x700)

## Technical Notes

### ROS2 Integration
- When using `--use-topic`, the camera node is created once and reused across game restarts for efficient resource management.
- Supports ROS2 Humble or newer.
- The camera subscription thread runs in the background and is properly cleaned up on exit.

### Camera Resource Management
- In ROS2 mode, a single ROS node persists throughout the application lifetime.
- When restarting the game, only detections are cleared—the camera connection is maintained.
- This prevents resource accumulation and speeds up game restarts.

## Simulation (Gazebo)

This repository includes a full Gazebo Classic simulation of the drone in a small warehouse world with 40 QR box markers.

### Prerequisites

- ROS 2 Humble
- Gazebo Classic 11 (`gazebo11`, `ros-humble-gazebo-ros-pkgs`)
- NumPy < 2 (required by `cv_bridge` compiled for ROS Humble):
  ```bash
  pip install "numpy<2"
  ```

### Submodules Setup

The simulation workspace uses two git submodules:

- [`sim_ws/src/small-warehouse-world`](https://github.com/FLW-TUDO/small-warehouse-world) — warehouse world with QR box markers (`ros2-devel` branch)
- [`sim_ws/src/sjtu_drone`](https://github.com/aaronxavier/sjtu_drone) — drone URDF, plugins, and bringup

Clone with submodules:
```bash
git clone --recurse-submodules <repo-url>
```

Or, if already cloned:
```bash
git submodule update --init --recursive
```

### Building the Simulation Workspace

```bash
cd sim_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
```

### Gazebo Environment Variables

Source the Gazebo Classic setup before launching to ensure shaders and plugins load correctly:

```bash
source /usr/share/gazebo-11/setup.sh
```

This sets `GAZEBO_RESOURCE_PATH`, `OGRE_RESOURCE_PATH`, and `GAZEBO_PLUGIN_PATH`. Add it to your shell startup file to avoid doing it manually each time.

### Launching the Simulation

```bash
source /opt/ros/humble/setup.bash
source sim_ws/install/setup.bash
ros2 launch sjtu_drone_bringup sjtu_drone_bringup.launch.py \
    world:=$(pwd)/sim_ws/src/small-warehouse-world/worlds/no_wall_no_roof_small_warehouse/no_wall_no_roof_small_warehouse.world \
    use_gui:=false \
    controller:=joystick
```

This launches gzserver (headless), spawns the drone, starts the joystick teleop node, and opens RViz.

### Running the Game with the Simulation

Once the simulation is running, launch the game subscribing to the drone's front camera:

```bash
source /opt/ros/humble/setup.bash
python3 main.py --use-topic /simple_drone/front/image_raw
```

The bottom camera is also available at `/simple_drone/bottom/image_raw`.

## Notes
- To use ROS2, source your ROS2 environment before running the game.
- The game window is resizable and the UI adapts accordingly.
- QR codes must be clearly visible to the camera for detection and decoding.
- Green bounding boxes appear around successfully detected and decoded QR codes.
- Each unique QR code is counted only once per game session.
