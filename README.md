# YAX_JEJU: 1/5-Scale Autonomous Driving Vehicle Project

This repository is a ROS 2 workspace for a student/team project on a 1/5-scale autonomous driving vehicle. It includes perception, decision, and integration components used for real-vehicle testing, with a focus on camera-based lane perception and LiDAR-based obstacle handling.

## Key Features
- Camera perception pipeline with YOLO nodes and lane information extraction
- LiDAR processing and obstacle detection nodes
- Mission/control nodes for waypoint, lane, tunnel, and obstacle behaviors
- Integrated launch flows across perception, decision, GPS/NTRIP, and serial communication

## Tech Stack
- ROS 2 (Python `rclpy` and C++ `rclcpp` components)
- Python, C++
- Ultralytics YOLO, OpenCV, NumPy
- YDLiDAR ROS 2 driver
- GPS/NTRIP-related ROS packages (`ublox_gps`, `ntrip_client`, `fix2nmea`)

## How to Run (Reference)
The exact runtime setup depends on hardware and external ROS dependencies. The commands below are the repository's launch entry points.

```bash
cd yax_jeju
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

```bash
# Camera + YOLO lane perception pipeline
ros2 launch camera_perception_pkg camera_lane.launch.py

# Mission/control integration nodes
ros2 launch my_custom_pkg mission_launch.py

# Full integrated launch used in this workspace
ros2 launch launch_pkg 2026ev_launch.py
```

## Repository Structure
- `src/camera_perception_pkg`: camera and YOLO-based perception nodes
- `src/lidar_perception_pkg`: LiDAR processing and obstacle-related nodes
- `src/decision_making_pkg`, `src/my_custom_pkg`: planning/control and mission logic
- `src/launch_pkg`: integrated launch files
- `src/interfaces_pkg`: custom ROS message interfaces

## Notes
- This repository reflects team development/integration work, not a standalone commercial product.
- Build/install/log artifacts are included in the workspace.
