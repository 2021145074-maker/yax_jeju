#!/usr/bin/env python3
"""
cone_camera_node
================
Camera-based cone driving with a chain-based centerline planner.

Pipeline:
  1) Orange cone mask (HSV-based with LAB/RGB support)
  2) Contour filtering -> cone foot points
  3) BEV transform
  4) Cone chain extraction
  5) Left/right boundary tracking across frames
  6) Midline generation (both boundaries or single-boundary fallback)
  7) Smoothed steering output
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

        # Parameters
        self.timer_period = float(
            self.declare_parameter('timer_period', 0.1).value)
        self.sub_image_topic = str(
            self.declare_parameter('sub_image_topic', '/camera/image_raw').value)

        # BEV transform params
        self.bev_src_points = self.declare_parameter(
            'bev_src_points', [100, 480, 540, 480, 400, 300, 240, 300]).value
        self.bev_dst_points = self.declare_parameter(
            'bev_dst_points', [150, 400, 250, 400, 250, 0, 150, 0]).value
        self.bev_width = int(
            self.declare_parameter('bev_width', 400).value)
        self.bev_height = int(
            self.declare_parameter('bev_height', 400).value)
        self.bev_center_x = self.bev_width // 2

        # Orange color thresholds
        self.hsv_lower = self.declare_parameter(
            'hsv_lower', [5, 100, 100]).value
        self.hsv_upper = self.declare_parameter(
            'hsv_upper', [25, 255, 255]).value
        self.lab_lower = self.declare_parameter(
            'lab_lower', [100, 140, 160]).value
        self.lab_upper = self.declare_parameter(
            'lab_upper', [220, 200, 220]).value
        self.rgb_lower = self.declare_parameter(
            'rgb_lower', [180, 80, 0]).value
        self.rgb_upper = self.declare_parameter(
            'rgb_upper', [255, 180, 80]).value

        # Mask and contour robustness
        self.use_clahe = bool(
            self.declare_parameter('use_clahe', True).value)
        self.clahe_clip_limit = float(
            self.declare_parameter('clahe_clip_limit', 2.0).value)
        self.clahe_grid_size = int(
            self.declare_parameter('clahe_grid_size', 8).value)
        self.mask_use_hsv_fallback = bool(
            self.declare_parameter('mask_use_hsv_fallback', True).value)
        self.mask_open_kernel = int(
            self.declare_parameter('mask_open_kernel', 3).value)
        self.mask_close_kernel = int(
            self.declare_parameter('mask_close_kernel', 7).value)
        self.roi_top_ratio = float(
            self.declare_parameter('roi_top_ratio', 0.3).value)

        self.min_contour_area = int(
            self.declare_parameter('min_contour_area', 120).value)
        self.max_contour_area = int(
            self.declare_parameter('max_contour_area', 50000).value)
        self.min_bbox_height_px = int(
            self.declare_parameter('min_bbox_height_px', 8).value)
        self.min_aspect_ratio = float(
            self.declare_parameter('min_aspect_ratio', 0.7).value)  # h / w
        self.max_aspect_ratio = float(
            self.declare_parameter('max_aspect_ratio', 6.0).value)
        self.min_solidity = float(
            self.declare_parameter('min_solidity', 0.55).value)

        # Chain building/tracking
        self.min_chain_points = int(
            self.declare_parameter('min_chain_points', 2).value)
        self.chain_link_max_dist_px = float(
            self.declare_parameter('chain_link_max_dist_px', 80.0).value)
        self.chain_forward_min_step_px = float(
            self.declare_parameter('chain_forward_min_step_px', 3.0).value)
        self.chain_angle_limit_deg = float(
            self.declare_parameter('chain_angle_limit_deg', 85.0).value)
        self.chain_match_max_cost_px = float(
            self.declare_parameter('chain_match_max_cost_px', 120.0).value)
        self.lane_half_width_px = float(
            self.declare_parameter('lane_half_width_px', 35.0).value)
        self.lookahead_y_from_bottom_px = float(
            self.declare_parameter('lookahead_y_from_bottom_px', 120.0).value)

        # Control
        self.k_cone = float(
            self.declare_parameter('k_cone', 7.0).value)
        self.max_steering = float(
            self.declare_parameter('max_steering', 7.0).value)
        self.cone_speed = float(
            self.declare_parameter('cone_speed', 80.0).value)
        self.steer_alpha = float(
            self.declare_parameter('steer_alpha', 0.35).value)
        self.max_steer_delta = float(
            self.declare_parameter('max_steer_delta', 1.2).value)

        # Activation and fallback
        self.entry_count_threshold = int(
            self.declare_parameter('entry_count_threshold', 2).value)
        self.exit_count_threshold = int(
            self.declare_parameter('exit_count_threshold', 15).value)
        self.entry_confidence_threshold = float(
            self.declare_parameter('entry_confidence_threshold', 0.65).value)
        self.keep_confidence_threshold = float(
            self.declare_parameter('keep_confidence_threshold', 0.35).value)
        self.path_hold_frames = int(
            self.declare_parameter('path_hold_frames', 5).value)
        self.path_hold_speed_scale = float(
            self.declare_parameter('path_hold_speed_scale', 0.7).value)

        # Internal states
        self.latest_image = None
        self.is_active = False
        self._enter_cnt = 0
        self._exit_cnt = 0
        self._path_lost_cnt = 0
        self._last_steering = 0.0
        self._prev_left_chain = None
        self._prev_right_chain = None
        self.cv_bridge = CvBridge()

        # BEV transform matrix
        src = np.float32(self._parse_points(self.bev_src_points))
        dst = np.float32(self._parse_points(self.bev_dst_points))
        self.bev_matrix = cv2.getPerspectiveTransform(src, dst)

        # QoS
        qos_rel = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE, depth=1)

        # Publishers
        self.pub_steering = self.create_publisher(
            Float64, '/tunnel/steering', qos_rel)
        self.pub_speed = self.create_publisher(
            Float64, '/tunnel/speed', qos_rel)
        self.pub_active = self.create_publisher(
            Bool, '/tunnel/active', qos_rel)
        self.pub_debug_img = self.create_publisher(
            Image, '/cone_camera/debug_image', qos_rel)

        # Subscriber
        self.create_subscription(
            Image, self.sub_image_topic, self._image_cb, qos_rel)

        self.timer = self.create_timer(self.timer_period, self._control_loop)
        self.get_logger().info('ConeCameraNode(chain-based) started')

    # Utilities
    @staticmethod
    def _parse_points(flat_list):
        pts = []
        for i in range(0, len(flat_list), 2):
            pts.append([float(flat_list[i]), float(flat_list[i + 1])])
        return pts

    @staticmethod
    def _dist(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    @staticmethod
    def _chain_mean_x(chain):
        if not chain:
            return 0.0
        return float(np.mean([p[0] for p in chain]))

    @staticmethod
    def _chain_sorted_for_interp(chain):
        arr = sorted(chain, key=lambda p: p[1])  # y ascending
        ys = np.array([p[1] for p in arr], dtype=float)
        xs = np.array([p[0] for p in arr], dtype=float)
        return ys, xs

    def _image_cb(self, msg: Image):
        self.latest_image = msg

    # Mask detection
    def _enhance_for_mask(self, img_bgr):
        if not self.use_clahe:
            return img_bgr
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        grid = max(2, self.clahe_grid_size)
        clahe = cv2.createCLAHE(
            clipLimit=max(0.5, self.clahe_clip_limit),
            tileGridSize=(grid, grid))
        l2 = clahe.apply(l)
        merged = cv2.merge((l2, a, b))
        return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    def _detect_orange_mask(self, img_bgr):
        h, w = img_bgr.shape[:2]
        proc = self._enhance_for_mask(img_bgr)

        roi_top = int(h * self.roi_top_ratio)
        roi_mask = np.zeros((h, w), dtype=np.uint8)
        roi_mask[roi_top:, :] = 255

        hsv = cv2.cvtColor(proc, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(proc, cv2.COLOR_BGR2LAB)
        rgb = cv2.cvtColor(proc, cv2.COLOR_BGR2RGB)

        mask_hsv = cv2.inRange(
            hsv,
            np.array(self.hsv_lower, dtype=np.uint8),
            np.array(self.hsv_upper, dtype=np.uint8))
        mask_lab = cv2.inRange(
            lab,
            np.array(self.lab_lower, dtype=np.uint8),
            np.array(self.lab_upper, dtype=np.uint8))
        mask_rgb = cv2.inRange(
            rgb,
            np.array(self.rgb_lower, dtype=np.uint8),
            np.array(self.rgb_upper, dtype=np.uint8))

        strong = cv2.bitwise_and(mask_hsv, cv2.bitwise_or(mask_lab, mask_rgb))
        if self.mask_use_hsv_fallback:
            combined = cv2.bitwise_or(strong, mask_hsv)
        else:
            combined = strong
        combined = cv2.bitwise_and(combined, roi_mask)

        open_k = max(1, int(self.mask_open_kernel))
        close_k = max(1, int(self.mask_close_kernel))
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_k, open_k))
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close_k, close_k))
        combined = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel_open)
        combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel_close)
        return combined

    # Contour filtering
    def _find_cone_centers(self, mask):
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        centers = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < self.min_contour_area or area > self.max_contour_area:
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            if h < self.min_bbox_height_px or w <= 0:
                continue

            aspect = float(h) / float(max(1, w))
            if aspect < self.min_aspect_ratio or aspect > self.max_aspect_ratio:
                continue

            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)
            solidity = float(area) / float(max(1.0, hull_area))
            if solidity < self.min_solidity:
                continue

            cx = x + w // 2
            cy = y + h  # cone foot
            centers.append((cx, cy))
        return centers

    # BEV transform
    def _to_bev(self, points):
        if not points:
            return []
        pts = np.float32(points).reshape(-1, 1, 2)
        bev_pts = cv2.perspectiveTransform(pts, self.bev_matrix)
        result = []
        for pt in bev_pts.reshape(-1, 2):
            bx, by = float(pt[0]), float(pt[1])
            if 0 <= bx < self.bev_width and 0 <= by < self.bev_height:
                result.append((bx, by))
        return result

    # Chain extraction
    def _build_chains(self, points):
        if len(points) < self.min_chain_points:
            return []

        order = sorted(range(len(points)), key=lambda i: points[i][1], reverse=True)
        used = [False] * len(points)
        chains = []
        angle_limit = math.radians(self.chain_angle_limit_deg)

        for start_idx in order:
            if used[start_idx]:
                continue

            chain = [points[start_idx]]
            used[start_idx] = True

            while True:
                last = chain[-1]
                chain_angle = None
                if len(chain) >= 2:
                    prev = chain[-2]
                    chain_angle = math.atan2(last[1] - prev[1], last[0] - prev[0])

                best_idx = -1
                best_dist = self.chain_link_max_dist_px
                for i in order:
                    if used[i]:
                        continue
                    cand = points[i]

                    # Forward progression in BEV: toward smaller y
                    if cand[1] >= last[1] - self.chain_forward_min_step_px:
                        continue

                    d = self._dist(last, cand)
                    if d >= best_dist:
                        continue

                    if chain_angle is not None:
                        new_angle = math.atan2(cand[1] - last[1], cand[0] - last[0])
                        diff = abs(new_angle - chain_angle)
                        if diff > math.pi:
                            diff = 2 * math.pi - diff
                        if diff > angle_limit:
                            continue

                    best_idx = i
                    best_dist = d

                if best_idx < 0:
                    break

                chain.append(points[best_idx])
                used[best_idx] = True

            if len(chain) >= self.min_chain_points:
                chain.sort(key=lambda p: p[1], reverse=True)  # near -> far
                chains.append(chain)

        chains.sort(key=lambda c: len(c), reverse=True)
        return chains

    def _chain_match_cost(self, chain, prev_chain):
        if not chain or not prev_chain:
            return float('inf')
        c_near = chain[0]
        p_near = prev_chain[0]
        near_cost = self._dist(c_near, p_near)
        mean_cost = abs(self._chain_mean_x(chain) - self._chain_mean_x(prev_chain))
        return near_cost + 0.5 * mean_cost

    def _select_boundaries(self, chains):
        left_chain = None
        right_chain = None
        mode = 'none'
        matched_from_history = False

        if len(chains) >= 2:
            c1 = chains[0]
            c2 = chains[1]
            if self._chain_mean_x(c1) <= self._chain_mean_x(c2):
                left_chain, right_chain = c1, c2
            else:
                left_chain, right_chain = c2, c1
            mode = 'both'
        elif len(chains) == 1:
            chain = chains[0]
            mode = 'single'
            mean_x = self._chain_mean_x(chain)

            left_cost = self._chain_match_cost(chain, self._prev_left_chain)
            right_cost = self._chain_match_cost(chain, self._prev_right_chain)
            if min(left_cost, right_cost) <= self.chain_match_max_cost_px:
                matched_from_history = True
                if left_cost <= right_cost:
                    left_chain = chain
                else:
                    right_chain = chain
            else:
                if mean_x < self.bev_center_x:
                    left_chain = chain
                else:
                    right_chain = chain

        # Keep history for temporal identity
        if left_chain is not None:
            self._prev_left_chain = list(left_chain)
        if right_chain is not None:
            self._prev_right_chain = list(right_chain)

        return left_chain, right_chain, mode, matched_from_history

    # Midline generation
    def _build_midline(self, left_chain, right_chain, mode, matched_from_history):
        mid_points = []
        virtual_chain = []
        confidence = 0.0
        source = 'none'

        if left_chain and right_chain:
            l_ys, l_xs = self._chain_sorted_for_interp(left_chain)
            r_ys, r_xs = self._chain_sorted_for_interp(right_chain)
            y_min = max(float(l_ys.min()), float(r_ys.min()))
            y_max = min(float(l_ys.max()), float(r_ys.max()))

            if y_max - y_min >= 5.0:
                n = max(len(left_chain) + len(right_chain), 6)
                sample_ys = np.linspace(y_max, y_min, n)  # near -> far
                lx = np.interp(sample_ys, l_ys, l_xs)
                rx = np.interp(sample_ys, r_ys, r_xs)
                for sy, x_left, x_right in zip(sample_ys, lx, rx):
                    mid_points.append(((float(x_left) + float(x_right)) / 2.0, float(sy)))
                confidence = min(1.0, 0.55 + 0.06 * (len(left_chain) + len(right_chain)))
                source = 'both'
        elif left_chain or right_chain:
            side_chain = left_chain if left_chain is not None else right_chain
            is_left = left_chain is not None

            offset = self.lane_half_width_px if is_left else -self.lane_half_width_px
            boundary_offset = 2.0 * self.lane_half_width_px if is_left else -2.0 * self.lane_half_width_px

            for x, y in side_chain:
                mid_points.append((float(x + offset), float(y)))
                virtual_chain.append((float(x + boundary_offset), float(y)))

            base = 0.42 + 0.05 * len(side_chain)
            if matched_from_history:
                base += 0.1
            confidence = min(0.85, base)
            source = 'single_left' if is_left else 'single_right'

        mid_points.sort(key=lambda p: p[1], reverse=True)  # near -> far
        return mid_points, virtual_chain, confidence, source

    def _smooth_steering(self, raw_steering):
        # Rate limit first
        delta = raw_steering - self._last_steering
        delta = max(-self.max_steer_delta, min(self.max_steer_delta, delta))
        limited = self._last_steering + delta

        # Then low-pass filter
        alpha = max(0.0, min(1.0, self.steer_alpha))
        smoothed = alpha * limited + (1.0 - alpha) * self._last_steering
        smoothed = max(-self.max_steering, min(self.max_steering, smoothed))
        self._last_steering = smoothed
        return smoothed

    # Control loop
    def _control_loop(self):
        if self.latest_image is None:
            return

        try:
            img_bgr = self.cv_bridge.imgmsg_to_cv2(
                self.latest_image, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'image decode failed: {e}')
            return

        mask = self._detect_orange_mask(img_bgr)
        img_centers = self._find_cone_centers(mask)
        bev_points = self._to_bev(img_centers)
        chains = self._build_chains(bev_points)
        left_chain, right_chain, mode, matched_hist = self._select_boundaries(chains)
        mid_points, virtual_chain, confidence, src_mode = self._build_midline(
            left_chain, right_chain, mode, matched_hist)

        strong_detected = confidence >= self.entry_confidence_threshold and len(mid_points) >= 2
        weak_detected = confidence >= self.keep_confidence_threshold and len(mid_points) >= 2

        if strong_detected:
            self._enter_cnt += 1
            self._exit_cnt = 0
            if self._enter_cnt >= self.entry_count_threshold:
                self.is_active = True
        elif weak_detected and self.is_active:
            self._exit_cnt = 0
        else:
            self._enter_cnt = 0
            self._exit_cnt += 1
            if self._exit_cnt >= self.exit_count_threshold:
                self.is_active = False

        if not self.is_active:
            self._path_lost_cnt = 0
            self._publish_debug(
                img_bgr, mask, img_centers, bev_points, chains,
                left_chain, right_chain,
                mid_points=mid_points,
                target_point=None,
                virtual_chain=virtual_chain,
                confidence=confidence,
                source_mode=src_mode)
            self._pub_values(0.0, 0.0, False)
            return

        if len(mid_points) < 2:
            self._path_lost_cnt += 1
            hold_ok = self._path_lost_cnt <= self.path_hold_frames
            speed = self.cone_speed * self.path_hold_speed_scale if hold_ok else 0.0
            active = hold_ok
            self._publish_debug(
                img_bgr, mask, img_centers, bev_points, chains,
                left_chain, right_chain,
                mid_points=mid_points,
                target_point=None,
                virtual_chain=virtual_chain,
                confidence=confidence,
                source_mode='hold')
            self._pub_values(self._last_steering, speed, active)
            return

        self._path_lost_cnt = 0
        target_y = float(self.bev_height - self.lookahead_y_from_bottom_px)
        target_y = max(0.0, min(float(self.bev_height - 1), target_y))
        target = min(mid_points, key=lambda p: abs(p[1] - target_y))
        target_x, target_y = target

        offset = (target_x - self.bev_center_x) / float(max(1, self.bev_center_x))
        raw_steer = self.k_cone * offset
        raw_steer = max(-self.max_steering, min(self.max_steering, raw_steer))
        steering = self._smooth_steering(raw_steer)

        self._publish_debug(
            img_bgr, mask, img_centers, bev_points, chains,
            left_chain, right_chain,
            mid_points=mid_points,
            target_point=target,
            virtual_chain=virtual_chain,
            confidence=confidence,
            source_mode=src_mode)
        self._pub_values(steering, self.cone_speed, True)
        self.get_logger().info(
            f'[ConeCam] chains={len(chains)} src={src_mode} conf={confidence:.2f} '
            f'target=({target_x:.1f},{target_y:.1f}) steer={steering:.2f}',
            throttle_duration_sec=0.5)

    # Debug image
    def _draw_polyline(self, img, chain, color, thickness=2):
        if chain is None or len(chain) < 2:
            return
        for i in range(len(chain) - 1):
            p1 = (int(chain[i][0]), int(chain[i][1]))
            p2 = (int(chain[i + 1][0]), int(chain[i + 1][1]))
            cv2.line(img, p1, p2, color, thickness)

    def _publish_debug(self, img_bgr, mask, img_centers, bev_points, chains,
                       left_chain, right_chain, mid_points,
                       target_point, virtual_chain, confidence, source_mode):
        bev_img = cv2.warpPerspective(
            img_bgr, self.bev_matrix, (self.bev_width, self.bev_height))

        # Raw points
        for x, y in bev_points:
            cv2.circle(bev_img, (int(x), int(y)), 3, (200, 200, 200), -1)

        # All chain candidates
        chain_colors = [
            (255, 255, 0), (255, 0, 255), (0, 255, 255),
            (0, 128, 255), (255, 128, 0)
        ]
        for i, chain in enumerate(chains):
            c = chain_colors[i % len(chain_colors)]
            self._draw_polyline(bev_img, chain, c, 1)

        # Selected boundaries
        self._draw_polyline(bev_img, left_chain, (0, 255, 0), 3)
        self._draw_polyline(bev_img, right_chain, (0, 0, 255), 3)

        # Virtual opposite boundary for single-side case
        self._draw_polyline(bev_img, virtual_chain, (255, 200, 0), 2)

        # Midline
        self._draw_polyline(bev_img, mid_points, (0, 165, 255), 2)

        # Target
        if target_point is not None:
            tx, ty = int(target_point[0]), int(target_point[1])
            cv2.drawMarker(bev_img, (tx, ty), (0, 165, 255),
                           cv2.MARKER_CROSS, 15, 2)

        # Center line
        cv2.line(bev_img, (self.bev_center_x, 0),
                 (self.bev_center_x, self.bev_height), (100, 100, 100), 1)

        status = 'ACTIVE' if self.is_active else 'INACTIVE'
        color = (0, 255, 0) if self.is_active else (0, 0, 255)
        cv2.putText(
            bev_img,
            f'{status} chains:{len(chains)} src:{source_mode} conf:{confidence:.2f}',
            (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
        cv2.putText(
            bev_img, f'steer:{self._last_steering:.2f}',
            (8, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        img_debug = img_bgr.copy()
        for cx, cy in img_centers:
            cv2.circle(img_debug, (cx, cy), 5, (0, 255, 255), -1)

        mask_color = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        h_orig = img_debug.shape[0]
        h_bev = bev_img.shape[0]
        bev_resized = cv2.resize(bev_img, (int(self.bev_width * h_orig / h_bev), h_orig))
        mask_resized = cv2.resize(mask_color, (img_debug.shape[1], h_orig))

        debug_combined = np.hstack([img_debug, mask_resized, bev_resized])
        self.pub_debug_img.publish(
            self.cv_bridge.cv2_to_imgmsg(debug_combined, 'bgr8'))

    # Publish helper
    def _pub_values(self, steering: float, speed: float, active: bool):
        s = Float64()
        s.data = float(steering)
        self.pub_steering.publish(s)

        v = Float64()
        v.data = float(speed)
        self.pub_speed.publish(v)

        b = Bool()
        b.data = bool(active)
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
