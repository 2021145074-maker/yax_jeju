#!/usr/bin/env python3
"""아두이노 시리얼 통신 간단 테스트"""
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
time.sleep(2)  # 아두이노 리셋 대기

# 버퍼 비우기
ser.reset_input_buffer()

tests = [
    ("전진 테스트",  "s0l50r50\n"),
    ("정지",        "s0l0r0\n"),
    ("후진 테스트",  "s0l-50r-50\n"),
    ("정지",        "s0l0r0\n"),
    ("조향 1 테스트","s1l0r0\n"),
    ("조향 3 테스트","s3l0r0\n"),
    ("조향 5 테스트","s5l0r0\n"),
    ("정지+직진",   "s0l0r0\n"),
]

for label, cmd in tests:
    print(f"\n=== {label}: {cmd.strip()} ===")
    ser.write(cmd.encode())
    time.sleep(1.5)
    # 아두이노 디버그 출력 읽기
    while ser.in_waiting:
        line = ser.readline().decode(errors='ignore').strip()
        if line:
            print(f"  Arduino: {line}")

ser.write(b"s0l0r0\n")
ser.close()
print("\n테스트 완료")
