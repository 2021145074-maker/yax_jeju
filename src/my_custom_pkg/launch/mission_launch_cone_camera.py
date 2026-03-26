#!/usr/bin/env python3
"""
my_custom_pkg launch file (camera-cone mode).

This variant uses `cone_camera_node` instead of `tunnel_nav_node`
for cone-section driving.

Run:
  ros2 launch my_custom_pkg mission_launch_cone_camera.py
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('my_custom_pkg')
    params_file = os.path.join(pkg_share, 'config', 'params.yaml')

    return LaunchDescription([
        Node(
            package='my_custom_pkg',
            executable='waypoint_follower_node',
            name='waypoint_follower_node',
            parameters=[params_file],
            output='screen',
        ),
        Node(
            package='my_custom_pkg',
            executable='lane_detection_node',
            name='lane_detection_node',
            parameters=[params_file],
            output='screen',
        ),
        # Camera-based cone driving replaces LiDAR tunnel_nav_node
        Node(
            package='my_custom_pkg',
            executable='cone_camera_node',
            name='cone_camera_node',
            parameters=[params_file],
            output='screen',
        ),
        Node(
            package='my_custom_pkg',
            executable='obstacle_detect_node',
            name='obstacle_detect_node',
            parameters=[params_file],
            output='screen',
        ),
        Node(
            package='my_custom_pkg',
            executable='mission_controller_node',
            name='mission_controller_node',
            parameters=[params_file],
            output='screen',
        ),
    ])
