import json
import os

# Roboflow에서 다운받은 기본 폴더 구조
folders = ['train', 'valid', 'test']

for folder in folders:
    json_file = os.path.join(folder, '_annotations.coco.json')
    
    # 해당 폴더에 json 파일이 없으면 건너뜀
    if not os.path.exists(json_file):
        continue
        
    with open(json_file, 'r') as f:
        data = json.load(f)
        
    # 이미지 정보(너비, 높이, 파일명)와 클래스 ID 매핑
    images = {img['id']: img for img in data['images']}
    # COCO의 카테고리 ID를 YOLO에 맞게 0번부터 시작하도록 재정렬
    categories = {cat['id']: idx for idx, cat in enumerate(data['categories'])}
    
    for ann in data['annotations']:
        img_id = ann['image_id']
        img_info = images[img_id]
        img_w, img_h = img_info['width'], img_info['height']
        
        # 이미지 파일명과 동일한 이름의 .txt 파일 경로 생성
        txt_filename = os.path.splitext(img_info['file_name'])[0] + '.txt'
        txt_filepath = os.path.join(folder, txt_filename)
        
        class_id = categories[ann['category_id']]
        
        # 세그먼테이션 좌표(x1, y1, x2, y2...)가 없는 경우 예외 처리
        if not ann['segmentation']:
            continue
            
        segmentation = ann['segmentation'][0] 
        norm_seg = []
        
        # YOLO 포맷을 위해 픽셀 좌표를 이미지 크기 대비 0~1 사이의 비율로 정규화
        for i in range(0, len(segmentation), 2):
            x = segmentation[i] / img_w
            y = segmentation[i+1] / img_h
            norm_seg.extend([f"{x:.6f}", f"{y:.6f}"])
            
        # "클래스번호 x1 y1 x2 y2 ..." 형태로 작성
        line = f"{class_id} " + " ".join(norm_seg) + "\n"
        
        # 변환된 내용을 텍스트 파일에 이어쓰기
        with open(txt_filepath, 'a') as f_txt:
            f_txt.write(line)
            
    print(f"✅ {folder} 폴더 세그먼테이션 라벨 변환 완료!")