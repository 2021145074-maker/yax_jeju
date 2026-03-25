#!/usr/bin/env python3
"""
cone_camera_node
================
카메라 이미지에서 주황색 꼬깔콘을 RGB/HSV/LAB 색공간으로 검출하고,
Bird's-Eye View 변환 후 좌/우 콘 사이의 중앙 경로를 따라 조향합니다.

검출 로직:
  1. 카메라 이미지 수신
  2. HSV + LAB + RGB 마스크 교집합으로 주황색 영역 검출
  3. 컨투어 → 바운딩 박스 중심점 추출
  4. Bird's-Eye View 변환으로 실제 위치 추정
  5. 좌/우 콘 분류 → 가장 가까운 콘 쌍의 중앙으로 조향

Subscribed Topics:
  /camera/image_raw  (sensor_msgs/Image)

Published Topics:
  /tunnel/steering   (std_msgs/Float64)
  /tunnel/speed      (std_msgs/Float64)
  /tunnel/active     (std_msgs/Bool)
  /cone_camera/debug_image (sensor_msgs/Image) — 디버그 시각화
"""
import math
import numpy as np
import cv2
import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSProfile, QoSHistoryPolicy,
    QoSDurabilityPolicy, QoSReliabilityPolicy,
)
from sensor_msgs.msg import Image
from std_msgs.msg import Float64, Bool
from cv_bridge import CvBridge


class ConeCameraNode(Node):
    def __init__(self):
        super().__init__('cone_camera_node')

        # ═══════ 파라미터 ═══════
        self.timer_period = float(
            self.declare_parameter('timer_period', 0.1).value)

        # 카메라 토픽
        self.sub_image_topic = str(
            self.declare_parameter('sub_image_topic', '/camera/image_raw').value)

        # BEV 변환 파라미터 (이미지 좌표 → 실제 좌표)
        # 소스 포인트: 이미지에서 사다리꼴 영역 (좌하, 우하, 우상, 좌상)
        self.bev_src_points = self.declare_parameter(
            'bev_src_points', [100, 480, 540, 480, 400, 300, 240, 300]).value
        # 목적지 포인트: BEV 이미지에서 직사각형 영역
        self.bev_dst_points = self.declare_parameter(
            'bev_dst_points', [150, 400, 250, 400, 250, 0, 150, 0]).value
        self.bev_width = int(
            self.declare_parameter('bev_width', 400).value)
        self.bev_height = int(
            self.declare_parameter('bev_height', 400).value)

        # 콘 검출 — HSV 범위 (주황색)
        self.hsv_lower = self.declare_parameter(
            'hsv_lower', [5, 100, 100]).value
        self.hsv_upper = self.declare_parameter(
            'hsv_upper', [25, 255, 255]).value

        # 콘 검출 — LAB 범위 (주황색)
        self.lab_lower = self.declare_parameter(
            'lab_lower', [100, 140, 160]).value
        self.lab_upper = self.declare_parameter(
            'lab_upper', [220, 200, 220]).value

        # 콘 검출 — RGB 범위 (주황색)
        self.rgb_lower = self.declare_parameter(
            'rgb_lower', [180, 80, 0]).value
        self.rgb_upper = self.declare_parameter(
            'rgb_upper', [255, 180, 80]).value

        # 컨투어 필터링
        self.min_contour_area = int(
            self.declare_parameter('min_contour_area', 100).value)
        self.max_contour_area = int(
            self.declare_parameter('max_contour_area', 50000).value)

        # ROI: 이미지 상단 무시 (하늘 등)
        self.roi_top_ratio = float(
            self.declare_parameter('roi_top_ratio', 0.3).value)

        # 조향
        self.k_cone = float(
            self.declare_parameter('k_cone', 5.0).value)
        self.max_steering = float(
            self.declare_parameter('max_steering', 7.0).value)
        self.cone_speed = float(
            self.declare_parameter('cone_speed', 50.0).value)

        # 히스테리시스
        self.entry_count_threshold = int(
            self.declare_parameter('entry_count_threshold', 2).value)
        self.exit_count_threshold = int(
            self.declare_parameter('exit_count_threshold', 15).value)
        self.min_cones_per_side = int(
            self.declare_parameter('min_cones_per_side', 1).value)

        # BEV 중심 x좌표 (차량 위치)
        self.bev_center_x = self.bev_width // 2

        # ═══════ 내부 상태 ═══════
        self.latest_image = None
        self.is_active = False
        self._enter_cnt = 0
        self._exit_cnt = 0
        self._last_steering = 0.0
        self.cv_bridge = CvBridge()

        # BEV 변환 행렬 계산
        src = np.float32(self._parse_points(self.bev_src_points))
        dst = np.float32(self._parse_points(self.bev_dst_points))
        self.bev_matrix = cv2.getPerspectiveTransform(src, dst)

        # ═══════ QoS ═══════
        qos_rel = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE, depth=1)
        qos_best = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
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
            Image, '/cone_camera/debug_image', qos_rel)

        # ═══════ 서브스크라이버 ═══════
        self.create_subscription(
            Image, self.sub_image_topic, self._image_cb, qos_rel)

        # ═══════ 타이머 ═══════
        self.timer = self.create_timer(self.timer_period, self._control_loop)
        self.get_logger().info('ConeCameraNode 시작')

    # ────────── 유틸 ──────────
    @staticmethod
    def _parse_points(flat_list):
        """[x1,y1,x2,y2,...] → [(x1,y1),(x2,y2),...]"""
        pts = []
        for i in range(0, len(flat_list), 2):
            pts.append([float(flat_list[i]), float(flat_list[i + 1])])
        return pts

    # ────────── 이미지 콜백 ──────────
    def _image_cb(self, msg: Image):
        self.latest_image = msg

    # ────────── 주황색 콘 마스크 생성 ──────────
    def _detect_orange_mask(self, img_bgr):
        """RGB + HSV + LAB 3중 마스크의 교집합으로 주황색 검출"""
        h, w = img_bgr.shape[:2]

        # ROI: 상단 제거
        roi_top = int(h * self.roi_top_ratio)
        roi_mask = np.zeros((h, w), dtype=np.uint8)
        roi_mask[roi_top:, :] = 255

        # --- HSV ---
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        mask_hsv = cv2.inRange(
            hsv,
            np.array(self.hsv_lower, dtype=np.uint8),
            np.array(self.hsv_upper, dtype=np.uint8))

        # --- LAB ---
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        mask_lab = cv2.inRange(
            lab,
            np.array(self.lab_lower, dtype=np.uint8),
            np.array(self.lab_upper, dtype=np.uint8))

        # --- RGB (OpenCV는 BGR이므로 변환) ---
        rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        mask_rgb = cv2.inRange(
            rgb,
            np.array(self.rgb_lower, dtype=np.uint8),
            np.array(self.rgb_upper, dtype=np.uint8))

        # 3중 교집합 + ROI
        combined = mask_hsv & mask_lab & mask_rgb & roi_mask

        # 모폴로지 연산으로 노이즈 제거
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        combined = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel)
        combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel)

        return combined

    # ────────── 컨투어 → 콘 중심점 추출 ──────────
    def _find_cone_centers(self, mask):
        """마스크에서 컨투어를 찾고, 바운딩 박스 하단 중심 반환.
        Returns: list of (cx, cy) — 이미지 좌표"""
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        centers = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < self.min_contour_area or area > self.max_contour_area:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            # 바운딩 박스 하단 중심 (콘 밑바닥 = 실제 위치)
            cx = x + w // 2
            cy = y + h
            centers.append((cx, cy))

        return centers

    # ────────── BEV 변환 ──────────
    def _to_bev(self, points):
        """이미지 좌표 리스트 → BEV 좌표 리스트.
        Returns: list of (bev_x, bev_y)"""
        if not points:
            return []

        pts = np.float32(points).reshape(-1, 1, 2)
        bev_pts = cv2.perspectiveTransform(pts, self.bev_matrix)
        result = []
        for pt in bev_pts.reshape(-1, 2):
            bx, by = float(pt[0]), float(pt[1])
            # BEV 이미지 범위 내인 것만
            if 0 <= bx < self.bev_width and 0 <= by < self.bev_height:
                result.append((bx, by))
        return result

    # ────────── 제어 루프 ──────────
    def _control_loop(self):
        if self.latest_image is None:
            return

        # 이미지 디코딩
        try:
            img_bgr = self.cv_bridge.imgmsg_to_cv2(
                self.latest_image, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'이미지 변환 실패: {e}')
            return

        # 주황색 마스크
        mask = self._detect_orange_mask(img_bgr)

        # 콘 중심점 (이미지 좌표)
        img_centers = self._find_cone_centers(mask)

        # BEV 변환
        bev_centers = self._to_bev(img_centers)

        # 좌/우 분류 (BEV 중심 기준)
        left_cones = [(x, y) for x, y in bev_centers if x < self.bev_center_x]
        right_cones = [(x, y) for x, y in bev_centers if x >= self.bev_center_x]

        # 감지 판정
        both_detected = (len(left_cones) >= self.min_cones_per_side
                         and len(right_cones) >= self.min_cones_per_side)
        any_detected = (len(left_cones) >= self.min_cones_per_side
                        or len(right_cones) >= self.min_cones_per_side)

        # 히스테리시스
        if both_detected:
            self._enter_cnt += 1
            self._exit_cnt = 0
            if self._enter_cnt >= self.entry_count_threshold:
                self.is_active = True
        elif any_detected and self.is_active:
            self._exit_cnt = 0
        else:
            self._exit_cnt += 1
            self._enter_cnt = 0
            if self._exit_cnt >= self.exit_count_threshold:
                self.is_active = False

        if not self.is_active:
            self._publish_debug(img_bgr, mask, img_centers, bev_centers,
                                left_cones, right_cones)
            self._pub_values(0.0, 0.0, False)
            return

        # ── 조향 계산 ──
        # BEV에서 y가 큰 값 = 차량에서 가까움 → y 기준 내림차순 정렬
        left_cones.sort(key=lambda c: c[1], reverse=True)
        right_cones.sort(key=lambda c: c[1], reverse=True)

        mid_x = None

        if left_cones and right_cones:
            # 양쪽 다 있으면 가장 가까운 좌/우 콘의 중앙
            lc = left_cones[0]
            rc = right_cones[0]
            mid_x = (lc[0] + rc[0]) / 2.0
        elif right_cones:
            # 오른쪽만 → 왼쪽으로 회피
            rc = right_cones[0]
            mid_x = rc[0] - 30  # 콘에서 왼쪽으로 오프셋
        elif left_cones:
            # 왼쪽만 → 오른쪽으로 회피
            lc = left_cones[0]
            mid_x = lc[0] + 30  # 콘에서 오른쪽으로 오프셋
        else:
            self._publish_debug(img_bgr, mask, img_centers, bev_centers,
                                left_cones, right_cones)
            self._pub_values(self._last_steering, self.cone_speed, True)
            return

        # BEV 중심으로부터의 오프셋 → 조향
        # mid_x > center → 오른쪽으로 가야 함 → 양수 조향
        offset = (mid_x - self.bev_center_x) / self.bev_center_x  # -1 ~ +1 정규화
        steering = self.k_cone * offset
        steering = max(-self.max_steering, min(self.max_steering, steering))
        self._last_steering = steering

        self._publish_debug(img_bgr, mask, img_centers, bev_centers,
                            left_cones, right_cones, mid_x)
        self._pub_values(steering, self.cone_speed, True)
        self.get_logger().info(
            f'[ConeCam] L={len(left_cones)} R={len(right_cones)} '
            f'mid_x={mid_x:.0f} steer={steering:.2f}',
            throttle_duration_sec=0.5)

    # ────────── 디버그 이미지 ──────────
    def _publish_debug(self, img_bgr, mask, img_centers, bev_centers,
                       left_cones, right_cones, mid_x=None):
        """원본 + BEV + 마스크 합성 디버그 이미지"""
        # BEV 이미지 생성
        bev_img = cv2.warpPerspective(
            img_bgr, self.bev_matrix,
            (self.bev_width, self.bev_height))

        # BEV 위에 콘 표시
        for (x, y) in left_cones:
            cv2.circle(bev_img, (int(x), int(y)), 8, (0, 255, 0), 2)
            cv2.putText(bev_img, 'L', (int(x) - 5, int(y) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        for (x, y) in right_cones:
            cv2.circle(bev_img, (int(x), int(y)), 8, (0, 0, 255), 2)
            cv2.putText(bev_img, 'R', (int(x) - 5, int(y) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

        # 중앙선
        cv2.line(bev_img, (self.bev_center_x, 0),
                 (self.bev_center_x, self.bev_height), (100, 100, 100), 1)

        # 중앙점 표시
        if mid_x is not None:
            cv2.drawMarker(bev_img, (int(mid_x), self.bev_height // 2),
                           (255, 128, 0), cv2.MARKER_CROSS, 15, 2)

        # 상태 텍스트
        status = 'ACTIVE' if self.is_active else 'INACTIVE'
        color = (0, 255, 0) if self.is_active else (0, 0, 255)
        cv2.putText(bev_img, f'{status} L:{len(left_cones)} R:{len(right_cones)}',
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(bev_img, f'steer:{self._last_steering:.2f}',
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # 원본 이미지에 콘 중심 표시
        img_debug = img_bgr.copy()
        for (cx, cy) in img_centers:
            cv2.circle(img_debug, (cx, cy), 5, (0, 255, 255), -1)

        # 마스크를 컬러로
        mask_color = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        # 원본과 마스크를 가로로 합침 (높이 맞추기)
        h_orig = img_debug.shape[0]
        h_bev = bev_img.shape[0]
        # BEV를 원본 높이에 맞춤
        bev_resized = cv2.resize(bev_img, (int(self.bev_width * h_orig / h_bev), h_orig))
        mask_resized = cv2.resize(mask_color, (img_debug.shape[1], h_orig))

        # 3개 나란히 합침
        debug_combined = np.hstack([img_debug, mask_resized, bev_resized])

        self.pub_debug_img.publish(
            self.cv_bridge.cv2_to_imgmsg(debug_combined, 'bgr8'))

    # ────────── 퍼블리시 헬퍼 ──────────
    def _pub_values(self, steering: float, speed: float, active: bool):
        s = Float64(); s.data = float(steering)
        v = Float64(); v.data = float(speed)
        b = Bool(); b.data = active
        self.pub_steering.publish(s)
        self.pub_speed.publish(v)
        self.pub_active.publish(b)


def main(args=None):
    rclpy.init(args=args)
    node = ConeCameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node._pub_values(0.0, 0.0, False)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
