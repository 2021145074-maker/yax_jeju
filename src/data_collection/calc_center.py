#!/usr/bin/env python3
"""테스트 결과에서 cmd=0 안정 구간의 POT 평균 계산"""

# cmd=0인 모든 구간의 POT 값 (테스트 결과에서 추출)

# 1) 전진 테스트 (cmd=0, 초기)
pre_steering = [
    441, 441, 441, 441, 441, 416, 462, 467, 466, 465,
    464, 466, 506, 467, 467, 468, 467, 467, 467, 468,
    476, 467, 467, 467, 468, 467, 468, 469, 498, 468
]

# 2) 정지 1차 (cmd=0)
stop1 = [
    468, 467, 469, 469, 469, 469, 467, 468, 468, 468,
    469, 469, 468, 471, 473, 469, 468, 470, 475, 468,
    468, 468, 468, 468, 468, 468, 469, 468, 467, 468
]

# 3) 후진 테스트 (cmd=0)
reverse = [
    468, 468, 469, 468, 473, 468, 470, 469, 469, 470,
    467, 490, 469, 469, 470, 468, 470, 466, 465, 469,
    467, 470, 468, 469, 468, 469, 468, 467, 468, 468
]

# 4) 정지 2차 (cmd=0)
stop2 = [
    476, 469, 470, 468, 471, 468, 474, 467, 470, 469,
    468, 469, 470, 469, 467, 469, 468, 468, 470, 467,
    469, 469, 468, 469, 468, 469, 469, 468, 468
]

# 5) 조향 후 복귀 (cmd=0, 정지+직진)
post_steering = [
    236, 260, 306, 340, 368, 390, 411, 432, 434, 432,
    433, 433, 448, 433, 432, 431, 431, 433, 433, 432,
    432, 432, 434, 432, 433, 431, 432, 433, 431, 432
]

# 안정 구간만 (과도 상태 제외 - 처음 수 샘플은 이동 중)
# 전진 초반 과도 상태 제외 (처음 6샘플)
pre_stable = pre_steering[6:]
# 복귀 과도 상태 제외 (처음 7샘플 = 모터 이동 중)
post_stable = post_steering[7:]

import statistics

all_stable_pre = pre_stable + stop1 + reverse + stop2
all_stable_post = post_stable

print("=== 조향 전 안정 구간 ===")
print(f"  샘플 수: {len(all_stable_pre)}")
print(f"  평균: {statistics.mean(all_stable_pre):.1f}")
print(f"  중앙값: {statistics.median(all_stable_pre):.1f}")
print(f"  최소/최대: {min(all_stable_pre)} / {max(all_stable_pre)}")

print("\n=== 조향 후 복귀 안정 구간 ===")
print(f"  샘플 수: {len(all_stable_post)}")
print(f"  평균: {statistics.mean(all_stable_post):.1f}")
print(f"  중앙값: {statistics.median(all_stable_post):.1f}")
print(f"  최소/최대: {min(all_stable_post)} / {max(all_stable_post)}")

overall = all_stable_pre + all_stable_post
print("\n=== 전체 통합 ===")
print(f"  샘플 수: {len(overall)}")
print(f"  평균: {statistics.mean(overall):.1f}")
print(f"  중앙값: {statistics.median(overall):.1f}")

center = round(statistics.mean(overall))
print(f"\n>>> 추천 RES_CENTER = {center}")
