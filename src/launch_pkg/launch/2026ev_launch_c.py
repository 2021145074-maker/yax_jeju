import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    # --- package share directories ---
    ublox_gps_pkg = get_package_share_directory('ublox_gps')
    ntrip_client_pkg = get_package_share_directory('ntrip_client')
    camera_perception_pkg = get_package_share_directory('camera_perception_pkg')
    ydlidar_pkg = get_package_share_directory('ydlidar_ros2_driver')
    my_custom_pkg = get_package_share_directory('my_custom_pkg')

    # --- external package launch & nodes ---
    ublox_gps_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ublox_gps_pkg, 'launch', 'ublox_gps_node-launch.py')
        )
    )
    ntrip_client_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ntrip_client_pkg, 'ntrip_client_launch.py')
        )
    )
    fix2nmea_node = Node(
        package='fix2nmea',
        executable='fix2nmea',
        name='fix2nmea_node'
    )
    camera_lane_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(camera_perception_pkg, 'launch', 'camera_lane.launch.py')
        )
    )
    path_planner_node = Node(
        package='decision_making_pkg',
        executable='path_planner_node',
        name='path_planner_node',
    )
    ydlidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ydlidar_pkg, 'launch', 'ydlidar_launch_view.py')
        )
    )

    # mission launch variant that uses cone_camera_node instead of tunnel_nav_node
    js_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(my_custom_pkg, 'launch', 'mission_launch_cone_camera.py')
        )
    )

    return LaunchDescription([
        ublox_gps_launch,
        ntrip_client_launch,
        fix2nmea_node,
        camera_lane_launch,
        path_planner_node,
        ydlidar_launch,
        js_launch
    ])
