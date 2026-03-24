#!/usr/bin/env python3
"""
tunnel_nav_node  (꼬깔콘 주행 모드)
====================================
LiDAR 스캔 데이터에서 꼬깔콘(소형 장애물)을 클러스터링하여 감지하고,
좌/우 콘 사이 중앙을 따라 주행합니다.

감지 로직:
  1. LiDAR 스캔 → 유효 포인트를 XY 좌표로 변환
  2. 인접 포인트 클러스터링 (DBSCAN 방식)
  3. 클러스터 폭이 콘 크기 범위 내인 것만 콘으로 인식
  4. 콘을 좌/우로 분류 → 가장 가까운 좌/우 콘 쌍의 중앙으로 조향

Subscribed Topics:
  /scan  (sensor_msgs/LaserScan)

Published Topics:
  /tunnel/steering  (std_msgs/Float64)
  /tunnel/speed     (std_msgs/Float64)
  /tunnel/active    (std_msgs/Bool)
"""
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSProfile, QoSHistoryPolicy,
    QoSDurabilityPolicy, QoSReliabilityPolicy,
)
import numpy as np
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64, Bool


class TunnelNavNode(Node):
    def __init__(self):
        super().__init__('tunnel_nav_node')

        # ═══════ 파라미터 ═══════
        self.sub_lidar_topic = self.declare_parameter(
            'sub_lidar_topic', '/scan').value
        self.timer_period = float(
            self.declare_parameter('timer_period', 0.1).value)

        # 콘 감지 범위 (m) — 이 거리 안의 물체만 탐색
        self.cone_detect_dist_m = float(
            self.declare_parameter('cone_detect_dist_m', 3.0).value)

        # 스캔 각도 범위 (deg) — 전방 기준 좌우 탐색 범위
        self.scan_angle_deg = float(
            self.declare_parameter('scan_angle_deg', 90.0).value)

        # 클러스터링 파라미터
        self.cluster_gap_m = float(
            self.declare_parameter('cluster_gap_m', 0.15).value)  # 포인트 간 끊김 기준
        self.cone_min_width_m = float(
            self.declare_parameter('cone_min_width_m', 0.03).value)  # 콘 최소 폭
        self.cone_max_width_m = float(
            self.declare_parameter('cone_max_width_m', 0.5).value)   # 콘 최대 폭
        self.cone_min_points = int(
            self.declare_parameter('cone_min_points', 3).value)      # 클러스터 최소 포인트

        # 콘 구간 진입/이탈 기준
        self.min_cones_per_side = int(
            self.declare_parameter('min_cones_per_side', 1).value)

        # 조향 게인
        self.k_cone = float(
            self.declare_parameter('k_cone', 2.0).value)
        self.max_steering = float(
            self.declare_parameter('max_steering', 7.0).value)
        self.cone_speed = float(
            self.declare_parameter('cone_speed', 70.0).value)

        # 히스테리시스
        self.entry_count_threshold = int(
            self.declare_parameter('entry_count_threshold', 5).value)
        self.exit_count_threshold = int(
            self.declare_parameter('exit_count_threshold', 10).value)

        # 내부 상태
        self.latest_scan: LaserScan = None
        self.is_active = False
        self._enter_cnt = 0
        self._exit_cnt = 0

        # ═══════ QoS ═══════
        qos_best = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE, depth=1)
        qos_rel = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE, depth=1)

        # ═══════ 퍼블리셔 ═══════
        self.pub_steering = self.create_publisher(
            Float64, '/tunnel/steering', qos_rel)
        self.pub_speed = self.create_publisher(
            Float64, '/tunnel/speed', qos_rel)
        self.pub_active = self.create_publisher(
            Bool, '/tunnel/active', qos_rel)

        # ═══════ 서브스크라이버 ═══════
        self.create_subscription(
            LaserScan, self.sub_lidar_topic,
            self._scan_cb, qos_best)

        # ═══════ 타이머 ═══════
        self.timer = self.create_timer(self.timer_period, self._control_loop)
        self.get_logger().info('TunnelNavNode(꼬깔콘 모드) 시작')

    # ────────── LiDAR 콜백 ──────────
    def _scan_cb(self, msg: LaserScan):
        self.latest_scan = msg

    # ────────── 스캔 → XY 좌표 변환 ──────────
    def _scan_to_xy(self, msg: LaserScan):
        """전방 ±scan_angle_deg 내 유효 포인트를 (x, y, angle) 배열로 변환.
        x: 전방, y: 좌측 양수 (ROS 관례)"""
        ranges = np.array(msg.ranges, dtype=float)
        n = len(ranges)
        if n == 0:
            return np.empty((0, 3))

        angles = msg.angle_min + np.arange(n) * msg.angle_increment

        # 전방 ±scan_angle_deg 필터
        half_rad = math.radians(self.scan_angle_deg)
        mask_angle = np.abs(angles) <= half_rad

        # 유효 거리 필터
        mask_valid = (np.isfinite(ranges)
                      & (ranges > msg.range_min)
                      & (ranges < min(msg.range_max, self.cone_detect_dist_m)))

        mask = mask_angle & mask_valid
        r = ranges[mask]
        a = angles[mask]

        x = r * np.cos(a)
        y = r * np.sin(a)
        return np.column_stack([x, y, a])

    # ────────── 클러스터링 ──────────
    def _cluster_points(self, points: np.ndarray):
        """인접 포인트를 클러스터로 묶는다 (스캔 순서 기반).
        points: shape (N, 3) — x, y, angle (angle 기준 정렬 가정)
        Returns: list of np.ndarray (각 클러스터의 포인트들)
        """
        if len(points) == 0:
            return []

        # angle 기준 정렬
        order = np.argsort(points[:, 2])
        pts = points[order]

        clusters = []
        current = [pts[0]]

        for i in range(1, len(pts)):
            # 이전 포인트와의 유클리드 거리
            dx = pts[i, 0] - pts[i - 1, 0]
            dy = pts[i, 1] - pts[i - 1, 1]
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < self.cluster_gap_m:
                current.append(pts[i])
            else:
                clusters.append(np.array(current))
                current = [pts[i]]

        clusters.append(np.array(current))
        return clusters

    # ────────── 클러스터 → 콘 필터링 ──────────
    def _filter_cones(self, clusters):
        """콘 크기에 해당하는 클러스터만 남기고, 각 콘의 중심(x, y) 반환.
        Returns: list of (cx, cy)
        """
        cones = []
        for cl in clusters:
            if len(cl) < self.cone_min_points:
                continue
            # 클러스터 폭 = 양 끝 포인트 간 거리
            width = math.sqrt(
                (cl[-1, 0] - cl[0, 0]) ** 2 + (cl[-1, 1] - cl[0, 1]) ** 2)
            if self.cone_min_width_m <= width <= self.cone_max_width_m:
                cx = float(np.mean(cl[:, 0]))
                cy = float(np.mean(cl[:, 1]))
                cones.append((cx, cy))
        return cones

    # ────────── 제어 루프 ──────────
    def _control_loop(self):
        if self.latest_scan is None:
            self._pub_values(0.0, 0.0, False)
            return

        msg = self.latest_scan
        points = self._scan_to_xy(msg)
        clusters = self._cluster_points(points)
        cones = self._filter_cones(clusters)

        # 좌/우 분류 (y > 0: 좌측, y < 0: 우측)
        left_cones = [(x, y) for x, y in cones if y > 0]
        right_cones = [(x, y) for x, y in cones if y <= 0]

        detected = (len(left_cones) >= self.min_cones_per_side
                    and len(right_cones) >= self.min_cones_per_side)

        # 히스테리시스
        if detected:
            self._enter_cnt += 1
            self._exit_cnt = 0
            if self._enter_cnt >= self.entry_count_threshold:
                self.is_active = True
        else:
            self._exit_cnt += 1
            self._enter_cnt = 0
            if self._exit_cnt >= self.exit_count_threshold:
                self.is_active = False

        if not self.is_active:
            self._pub_values(0.0, 0.0, False)
            return

        # ── 조향 계산: 가장 가까운 좌/우 콘 쌍의 중앙 ──
        # 가장 가까운 콘 = 전방 거리(x) 기준
        left_cones.sort(key=lambda c: c[0])   # x 오름차순 (가까운 순)
        right_cones.sort(key=lambda c: c[0])

        # 가장 가까운 좌/우 콘
        lc = left_cones[0]
        rc = right_cones[0]

        # 중앙점
        mid_x = (lc[0] + rc[0]) / 2.0
        mid_y = (lc[1] + rc[1]) / 2.0

        # 차량 전방(x축) 대비 중앙점의 y 오프셋 → 조향
        # mid_y > 0 이면 중앙이 왼쪽 → 왼쪽으로 조향
        steering = self.k_cone * mid_y
        steering = max(-self.max_steering, min(self.max_steering, steering))

        self._pub_values(steering, self.cone_speed, True)
        self.get_logger().info(
            f'[Cone] L={len(left_cones)}개 R={len(right_cones)}개 '
            f'mid=({mid_x:.2f},{mid_y:.2f}) steer={steering:.2f}',
            throttle_duration_sec=0.5)

    # ────────── 퍼블리시 헬퍼 ──────────
    def _pub_values(self, steering: float, speed: float, active: bool):
        s = Float64(); s.data = float(steering)
        self.pub_steering.publish(s)
        v = Float64(); v.data = float(speed)
        self.pub_speed.publish(v)
        b = Bool(); b.data = active
        self.pub_active.publish(b)


def main(args=None):
    rclpy.init(args=args)
    node = TunnelNavNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
