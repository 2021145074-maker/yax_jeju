from ultralytics import YOLO
import cv2

model = YOLO("/home/jsmoon/yax_jeju/best.pt")

print("task =", getattr(model, "task", "unknown"))
print("names =", model.names)

img = cv2.imread("/home/jsmoon/Desktop/yolo/test/images/20250704_170223_jpg.rf.a992f22c300c1ed5d4f88ca1f5a7cba0.jpg")  # 아무 테스트 이미지
res = model(img, verbose=False)[0]

print("num_boxes =", 0 if res.boxes is None else len(res.boxes))
print("masks_is_none =", res.masks is None)
print("keypoints_is_none =", res.keypoints is None)