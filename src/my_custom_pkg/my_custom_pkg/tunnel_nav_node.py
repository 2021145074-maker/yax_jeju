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
import cv2
from sensor_msgs.msg import LaserScan, Image
from std_msgs.msg import Float64, Bool
from cv_bridge import CvBridge


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

        # 스캔 각도 범위 (deg) — 좌/우 개별 설정
        self.left_angle_min_deg = float(
            self.declare_parameter('left_angle_min_deg', 30.0).value)
        self.left_angle_max_deg = float(
            self.declare_parameter('left_angle_max_deg', 70.0).value)
        self.right_angle_min_deg = float(
            self.declare_parameter('right_angle_min_deg', -70.0).value)
        self.right_angle_max_deg = float(
            self.declare_parameter('right_angle_max_deg', -30.0).value)

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

        # 경로 생성 파라미터
        self.lane_half_width_m = float(
            self.declare_parameter('lane_half_width_m', 0.50).value)  # 콘 통로 반폭
        self.lookahead_m = float(
            self.declare_parameter('lookahead_m', 1.5).value)         # 전방 주시 거리
        self.cone_link_max_dist_m = float(
            self.declare_parameter('cone_link_max_dist_m', 1.5).value)  # 같은 경계 연결 최대 거리
        self.curve_gain = float(
            self.declare_parameter('curve_gain', 1.0).value)            # 1체인 곡률 증폭 (>1: 안쪽으로)
        self.chain_angle_limit_deg = float(
            self.declare_parameter('chain_angle_limit_deg', 80.0).value)  # 체인 확장 시 최대 꺾임 각도

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
        self._last_steering = 0.0

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
        self.pub_debug_img = self.create_publisher(
            Image, '/tunnel/debug_image', qos_rel)
        self.cv_bridge = CvBridge()

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
        """좌(+30~+70°) / 우(-70~-30°) 범위의 유효 포인트를 (x, y, angle) 배열로 변환.
        전방 ±30° 는 제외하여 obstacle_detect_node와 간섭을 줄임.
        x: 전방, y: 좌측 양수 (ROS 관례)"""
        ranges = np.array(msg.ranges, dtype=float)
        n = len(ranges)
        if n == 0:
            return np.empty((0, 3))

        angles = msg.angle_min + np.arange(n) * msg.angle_increment

        # 좌측 범위 OR 우측 범위
        left_min = math.radians(self.left_angle_min_deg)
        left_max = math.radians(self.left_angle_max_deg)
        right_min = math.radians(self.right_angle_min_deg)
        right_max = math.radians(self.right_angle_max_deg)

        mask_left = (angles >= left_min) & (angles <= left_max)
        mask_right = (angles >= right_min) & (angles <= right_max)
        mask_angle = mask_left | mask_right

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
            # 클러스터 폭 = 양 끝 포인트 간 거리
            width = math.sqrt(
                (cl[-1, 0] - cl[0, 0]) ** 2 + (cl[-1, 1] - cl[0, 1]) ** 2)
            cx = float(np.mean(cl[:, 0]))
            cy = float(np.mean(cl[:, 1]))
            self.get_logger().debug(
                f'  cluster: pts={len(cl)} width={width:.3f}m '
                f'center=({cx:.2f},{cy:.2f})',
                throttle_duration_sec=0.5)
            if len(cl) < self.cone_min_points:
                continue
            if self.cone_min_width_m <= width <= self.cone_max_width_m:
                cones.append((cx, cy))
        return cones

    # ────────── 콘 → 경계 체인 생성 ──────────
    def _build_chains(self, cones):
        """콘 간 거리가 cone_link_max_dist_m 이내면 같은 경계로 연결.
        좌/우 개념 없이 거리 기반으로 체인을 생성.
        Returns: list of chains — 각 체인은 [(x, y), ...] (x 오름차순)
        """
        if not cones:
            return []

        max_dist = self.cone_link_max_dist_m
        assigned = [False] * len(cones)
        chains = []

        # 가장 가까운(x 최소) 콘부터 시작
        sorted_indices = sorted(range(len(cones)), key=lambda i: cones[i][0])

        for start_idx in sorted_indices:
            if assigned[start_idx]:
                continue

            # 새 체인 시작
            chain = [cones[start_idx]]
            assigned[start_idx] = True

            # 체인 확장: 마지막 콘에서 가장 가까운 미할당 콘을 반복 연결
            # 단, 기존 체인 방향 대비 ±chain_angle_limit_deg 이내만 허용
            angle_limit_rad = math.radians(self.chain_angle_limit_deg)

            while True:
                last = chain[-1]
                best_idx = -1
                best_dist = max_dist

                # 체인 방향 계산 (콘이 2개 이상이면 마지막 두 콘의 방향)
                if len(chain) >= 2:
                    prev = chain[-2]
                    chain_angle = math.atan2(last[1] - prev[1],
                                             last[0] - prev[0])
                else:
                    chain_angle = None

                for i in sorted_indices:
                    if assigned[i]:
                        continue
                    d = math.hypot(cones[i][0] - last[0],
                                   cones[i][1] - last[1])
                    if d < best_dist:
                        # 각도 제한 검사
                        if chain_angle is not None:
                            new_angle = math.atan2(cones[i][1] - last[1],
                                                   cones[i][0] - last[0])
                            diff = abs(new_angle - chain_angle)
                            if diff > math.pi:
                                diff = 2 * math.pi - diff
                            if diff > angle_limit_rad:
                                continue
                        best_dist = d
                        best_idx = i

                if best_idx < 0:
                    break

                chain.append(cones[best_idx])
                assigned[best_idx] = True

            chain.sort(key=lambda c: c[0])
            chains.append(chain)

        return chains

    # ────────── 체인 → 중앙선 생성 ──────────
    def _build_midline(self, chains):
        """경계 체인들로부터 주행 중앙선을 계산.
        2개 체인: 두 경계 사이 중앙
        1개 체인: 체인을 차량 위치(y=0)로 평행이동 → 형태(곡률)로 조향
        Returns: list of (x, y)
        """
        if not chains:
            return []

        if len(chains) >= 2:
            # 콘 수가 가장 많은 2개 체인을 경계로 사용
            chains.sort(key=lambda c: len(c), reverse=True)
            c1 = chains[0]
            c2 = chains[1]

            c1_xs = [c[0] for c in c1]
            c1_ys = [c[1] for c in c1]
            c2_xs = [c[0] for c in c2]
            c2_ys = [c[1] for c in c2]

            x_lo = min(min(c1_xs), min(c2_xs))
            x_hi = max(max(c1_xs), max(c2_xs))
            sample_xs = np.linspace(x_lo, x_hi, max(len(c1) + len(c2), 5))

            mid_points = []
            for sx in sample_xs:
                y1 = float(np.interp(sx, c1_xs, c1_ys))
                y2 = float(np.interp(sx, c2_xs, c2_ys))
                mid_points.append((float(sx), (y1 + y2) / 2.0))
            return mid_points

        # 1개 체인 → 가장 가까운 콘의 y를 빼서 차량 위치로 평행이동
        # 체인의 형태(곡률)만으로 조향 방향 결정, curve_gain으로 곡률 증폭
        chain = chains[0]
        anchor_y = chain[0][1]  # x 최소(가장 가까운) 콘의 y

        mid_points = [(c[0], (c[1] - anchor_y) * self.curve_gain) for c in chain]
        mid_points.sort(key=lambda p: p[0])
        return mid_points

    # ────────── 제어 루프 ──────────
    def _control_loop(self):
        if self.latest_scan is None:
            self._pub_values(0.0, 0.0, False)
            return

        msg = self.latest_scan
        points = self._scan_to_xy(msg)
        clusters = self._cluster_points(points)
        cones = self._filter_cones(clusters)

        self.get_logger().info(
            f'[Debug] points={len(points)} clusters={len(clusters)} cones={len(cones)}',
            throttle_duration_sec=1.0)

        # 경계 체인 생성 (거리 기반, 좌/우 구분 없음)
        cone_chains = self._build_chains(cones)

        # 히스테리시스: 2개 체인이면 진입, 1개라도 있으면 유지
        has_two = len(cone_chains) >= 2
        has_any = len(cone_chains) >= 1 and len(cones) >= self.min_cones_per_side

        if has_two:
            self._enter_cnt += 1
            self._exit_cnt = 0
            if self._enter_cnt >= self.entry_count_threshold:
                self.is_active = True
        elif has_any and self.is_active:
            self._exit_cnt = 0
        else:
            self._exit_cnt += 1
            self._enter_cnt = 0
            if self._exit_cnt >= self.exit_count_threshold:
                self.is_active = False

        if not self.is_active:
            self._publish_debug_image(points, clusters, cones,
                                       cone_chains)
            self._pub_values(0.0, 0.0, False)
            return

        # ── 경로 중앙선 기반 조향 ──
        mid_points = self._build_midline(cone_chains)

        if not mid_points:
            self._publish_debug_image(points, clusters, cones,
                                       cone_chains)
            self._pub_values(self._last_steering, self.cone_speed, True)
            return

        # lookahead 지점 선택
        target = min(mid_points, key=lambda p: abs(p[0] - self.lookahead_m))
        mid_x, mid_y = target

        steering = self.k_cone * mid_y
        steering = max(-self.max_steering, min(self.max_steering, steering))
        self._last_steering = steering

        self._publish_debug_image(points, clusters, cones,
                                   cone_chains, mid_x, mid_y, mid_points)
        self._pub_values(steering, self.cone_speed, True)
        self.get_logger().info(
            f'[Cone] chains={len(cone_chains)} cones={len(cones)} '
            f'target=({mid_x:.2f},{mid_y:.2f}) steer={steering:.2f}',
            throttle_duration_sec=0.5)

    # ────────── 디버그 이미지 ──────────
    def _publish_debug_image(self, points, clusters, cones,
                              cone_chains=None,
                              mid_x=None, mid_y=None,
                              mid_points=None):
        """Bird's-eye view 디버그 이미지 퍼블리시.
        이미지 중앙 하단 = 차량 위치, 위쪽 = 전방"""
        IMG_SIZE = 400
        SCALE = 100  # 1m = 100px
        cx, cy_img = IMG_SIZE // 2, IMG_SIZE - 30  # 차량 위치
        if cone_chains is None:
            cone_chains = []

        img = np.zeros((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8)

        # 그리드 (1m 간격)
        for r in range(1, int(self.cone_detect_dist_m) + 2):
            cv2.circle(img, (cx, cy_img), r * SCALE, (40, 40, 40), 1)

        # 스캔 각도 범위 표시
        for ang_deg in [self.left_angle_min_deg, self.left_angle_max_deg,
                        self.right_angle_min_deg, self.right_angle_max_deg]:
            rad = math.radians(ang_deg)
            ex = int(cx + 300 * math.sin(rad))
            ey = int(cy_img - 300 * math.cos(rad))
            cv2.line(img, (cx, cy_img), (ex, ey), (60, 60, 60), 1)

        # 전체 LiDAR 포인트 (회색 점)
        for pt in points:
            px = int(cx + pt[1] * SCALE)
            py = int(cy_img - pt[0] * SCALE)
            if 0 <= px < IMG_SIZE and 0 <= py < IMG_SIZE:
                cv2.circle(img, (px, py), 2, (100, 100, 100), -1)

        # 클러스터 (각각 다른 색)
        cluster_colors = [(0, 255, 255), (255, 0, 255), (255, 255, 0),
                          (0, 128, 255), (255, 128, 0), (128, 255, 0)]
        for i, cl in enumerate(clusters):
            color = cluster_colors[i % len(cluster_colors)]
            for pt in cl:
                px = int(cx + pt[1] * SCALE)
                py = int(cy_img - pt[0] * SCALE)
                if 0 <= px < IMG_SIZE and 0 <= py < IMG_SIZE:
                    cv2.circle(img, (px, py), 3, color, -1)

        # 경계 체인별 콘 + 연결선 (체인마다 다른 색)
        chain_colors = [(0, 255, 0), (0, 0, 255), (255, 255, 0),
                        (255, 0, 255), (0, 255, 255)]
        for ci, chain in enumerate(cone_chains):
            color = chain_colors[ci % len(chain_colors)]
            # 콘 원
            for (cone_x, cone_y) in chain:
                px = int(cx + cone_y * SCALE)
                py = int(cy_img - cone_x * SCALE)
                if 0 <= px < IMG_SIZE and 0 <= py < IMG_SIZE:
                    cv2.circle(img, (px, py), 8, color, 2)
                    cv2.putText(img, str(ci), (px - 5, py - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            # 연결선
            if len(chain) >= 2:
                for i in range(len(chain) - 1):
                    p1 = (int(cx + chain[i][1] * SCALE),
                          int(cy_img - chain[i][0] * SCALE))
                    p2 = (int(cx + chain[i+1][1] * SCALE),
                          int(cy_img - chain[i+1][0] * SCALE))
                    cv2.line(img, p1, p2, color, 2)

        # 중앙선 (주황 선)
        if mid_points and len(mid_points) >= 2:
            for i in range(len(mid_points) - 1):
                p1 = (int(cx + mid_points[i][1] * SCALE),
                      int(cy_img - mid_points[i][0] * SCALE))
                p2 = (int(cx + mid_points[i+1][1] * SCALE),
                      int(cy_img - mid_points[i+1][0] * SCALE))
                cv2.line(img, p1, p2, (0, 165, 255), 2)

        # 타겟 포인트 (주황 X)
        if mid_x is not None and mid_y is not None:
            px = int(cx + mid_y * SCALE)
            py = int(cy_img - mid_x * SCALE)
            if 0 <= px < IMG_SIZE and 0 <= py < IMG_SIZE:
                cv2.drawMarker(img, (px, py), (0, 165, 255),
                               cv2.MARKER_CROSS, 15, 2)

        # 차량 위치 (흰 삼각형)
        pts_car = np.array([[cx, cy_img - 10], [cx - 7, cy_img + 5],
                            [cx + 7, cy_img + 5]], np.int32)
        cv2.fillPoly(img, [pts_car], (255, 255, 255))

        # 상태 텍스트
        status = 'ACTIVE' if self.is_active else 'INACTIVE'
        color_txt = (0, 255, 0) if self.is_active else (0, 0, 255)
        n_cones = sum(len(c) for c in cone_chains)
        cv2.putText(img, f'{status} chains:{len(cone_chains)} cones:{n_cones}',
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_txt, 1)
        cv2.putText(img, f'steer:{self._last_steering:.2f}',
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        self.pub_debug_img.publish(self.cv_bridge.cv2_to_imgmsg(img, 'bgr8'))

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
