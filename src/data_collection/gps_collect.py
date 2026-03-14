#!/usr/bin/env python3
import os
import time
import datetime
import csv
import serial
import sys
import tty
import termios
import threading
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

# --- Helper function for non-blocking keyboard input on Linux/macOS ---
def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class VehicleState:
    """ Thread-safe class to store the vehicle's live GPS state. """
    def __init__(self):
        self.lock = threading.Lock()
        self.latitude = 0.0
        self.longitude = 0.0

    def update_gps(self, lat, lon):
        with self.lock:
            self.latitude = lat
            self.longitude = lon
            
    def get_gps(self):
        with self.lock:
            return self.latitude, self.longitude

class DataCollector:
    """ Handles keyboard input for control values in a thread-safe manner. """
    def __init__(self, max_steering):
        self.max_steering = max_steering
        self.steering = 0
        self.speed = 0
        self.SPEED_STEP = 10
        self.MAX_SPEED = 100
        self.lock = threading.Lock()

    def update_controls(self, key):
        with self.lock:
            if key == 'w': self.speed = min(self.MAX_SPEED, self.speed + self.SPEED_STEP)
            elif key == 's': self.speed = max(-self.MAX_SPEED, self.speed - self.SPEED_STEP)
            elif key == 'a': self.steering = max(-self.max_steering, self.steering - 1)
            elif key == 'd': self.steering = min(self.max_steering, self.steering + 1)
            elif key == 'x': self.speed, self.steering = 0, 0

    def get_control_values(self):
        with self.lock:
            return {"steering": self.steering, "speed": self.speed}

class DataCollectorNode(Node):
    """ The main ROS 2 node for data collection. """
    def __init__(self):
        super().__init__('data_collector_node')

        # --- CONFIGURATION ---
        self.SAVE_FREQUENCY_HZ = 1
        CONTROL_SERIAL_PORT = "/dev/ttyUSB0"
        BAUD_RATE = 115200
        MAX_STEERING = 7
        
        # --- SETUP ---
        self.collector = DataCollector(max_steering=MAX_STEERING)
        self.vehicle_state = VehicleState()
        
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'camera_perception_pkg', 'camera_perception_pkg', 'lib', 'Collected_Datasets')
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        session_path = os.path.join(base_path, timestamp)
        os.makedirs(session_path, exist_ok=True)
        
        self.control_log_path = os.path.join(session_path, "driving_log.csv")
        self.gps_log_path = os.path.join(session_path, "gps_log.csv")
        self.get_logger().info(f"âœ… Saving data to: {timestamp}")

        try:
            self.ser = serial.Serial(CONTROL_SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(1)
        except serial.SerialException as e:
            self.get_logger().error(f"Error opening control port: {e}")
            raise e

        # --- Start Subscribers and Threads ---
        self.create_subscription(NavSatFix, '/ublox_gps_node/fix', self.gps_callback, 10)
        self.get_logger().info("âœ… Subscribed to /ublox_gps_node/fix")
        
        self.stop_event = threading.Event()
        self.keyboard_thread = threading.Thread(target=self.keyboard_listener, daemon=True)
        self.keyboard_thread.start()
        
        self.get_logger().info("Waiting for first GPS fix from ROS topic...")
        time.sleep(2) # Give time for connections

        self.timer = self.create_timer(1.0 / self.SAVE_FREQUENCY_HZ, self.timer_callback)

    def gps_callback(self, msg):
        if msg.status.status >= 0: # Check for a valid GPS fix
            self.vehicle_state.update_gps(msg.latitude, msg.longitude)

    def keyboard_listener(self):
        while not self.stop_event.is_set():
            key = get_key()
            if key == 'q':
                self.stop_event.set()
                rclpy.shutdown()
                break
            self.collector.update_controls(key)
    
    def timer_callback(self):
        """ This function runs at SAVE_FREQUENCY_HZ. """
        controls = self.collector.get_control_values()
        steering, speed = controls['steering'], controls['speed']
        
        lat, lon = self.vehicle_state.get_gps()
        
        if lat == 0.0:
            self.get_logger().info('Waiting for GPS fix...', throttle_duration_sec=1)
            return

        # Append data to respective CSV files
        with open(self.control_log_path, 'a', newline='') as f:
            csv.writer(f).writerow([steering, speed, speed])
        with open(self.gps_log_path, 'a', newline='') as f:
            csv.writer(f).writerow([lat, lon])
        
        message = f"s{int(steering)}l{speed}r{speed}\n"
        self.ser.write(message.encode())
        
        status = f"Steering: {steering:>2}, Speed: {speed:>4} | GPS: ({lat:.6f}, {lon:.6f})"
        sys.stdout.write('\r' + status)
        sys.stdout.flush()

    def on_shutdown(self):
        """ Cleans up resources when the node is shut down. """
        self.get_logger().info("\n\nStopping device and saving data...")
        if self.ser.is_open:
            self.ser.write(b"s0l0r0\n")
            time.sleep(0.1)
            self.ser.close()
        self.get_logger().info("Done.")

def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        # Create headers for CSV files
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'camera_perception_pkg', 'camera_perception_pkg', 'lib', 'Collected_Datasets')
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        session_path = os.path.join(base_path, timestamp)
        os.makedirs(session_path, exist_ok=True)
        control_log_path = os.path.join(session_path, "driving_log.csv")
        gps_log_path = os.path.join(session_path, "gps_log.csv")
        with open(control_log_path, 'w', newline='') as f: csv.writer(f).writerow(['steering', 'left_speed', 'right_speed'])
        with open(gps_log_path, 'w', newline='') as f: csv.writer(f).writerow(['latitude', 'longitude'])

        node = DataCollectorNode()
        print("\n--- Starting ROS 2 Data Collection ---")
        print("Use w/a/s/d to drive. Press 'q' to quit.")
        rclpy.spin(node)
    except Exception as e:
        if node: node.get_logger().error(f"An error occurred: {e}")
    finally:
        if node:
            node.on_shutdown()
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
