from ultralytics import YOLO
import torch

def main():
    # 1. GPU 체크
    if torch.cuda.is_available():
        print(f"🚀 GPU 가속 활성화: {torch.cuda.get_device_name(0)}")
    else:
        print("❌ GPU를 찾을 수 없습니다. CUDA 세팅을 확인해주세요!")
        return

    # 2. 모델 로드 (중요: 반드시 '-seg'가 붙은 세그먼테이션 전용 모델을 사용해야 합니다)
    model = YOLO('yolov8s-seg.pt')

    # 3. 모델 학습
    print("--- 🛣️ 차선 세그먼테이션 학습을 시작합니다 ---")
    results = model.train(
        data='data.yaml', 
        epochs=100, 
        imgsz=640, 
        batch=16, # RTX 4060 8GB VRAM에 안정적인 배치 사이즈
        device=0,
        patience=20, 
        name='lane_segmentation_v1'
    )

    # 4. 모델 평가
    print("--- 📊 검증 데이터를 통한 평가 ---")
    metrics = model.val()
    
    # 박스(Box)가 아닌 마스크(Mask) mAP 점수를 확인하는 것이 차선 인식의 핵심입니다.
    print(f"Mask mAP50-95: {metrics.seg.map:.4f}")

    # 5. TensorRT 엔진 변환
    print("--- ⚡ 실시간 제어를 위한 TensorRT 엔진 변환 ---")
    model.export(
        format='engine', 
        half=True, 
        device=0,
        workspace=4 
    )
    print("--- 🎉 모든 학습 파이프라인 완료! ---")

if __name__ == '__main__':
    main()