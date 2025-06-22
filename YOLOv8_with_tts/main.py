from ultralytics import YOLO
import cv2
from tts_module import speak  # tts.py의 함수 import
from tts_module import screen_messages  # 화면별 멘트 정의 가져오기
from tts_module import determine_screen_type  # 화면 종류 유추 함수 import
from tts_module import translate_label  # 라벨 한글화 함수 import

# from flask import Flask, request, jsonify
# import openai
# import base64


# 바운딩박스의 좌표값을 받아 전체 영역에서의 대략적 위치로 변환
def get_position_label(center_x, center_y, img_width, img_height):
    x_ratio = center_x / img_width
    y_ratio = center_y / img_height


    

    # # 위/중/아래
    # if y_ratio < 0.33:
    #     position += "상단"
    # elif y_ratio > 0.66:
    #     position += "하단"

    # 좌/중/우
    # if x_ratio < 0.33:
    #     position += " 좌측"
    # elif x_ratio > 0.66:
    #     position += " 우측"
    # elif 0.33 <= x_ratio <= 0.66 and 0.33 <= y_ratio <= 0.66:
    #     position += " 중앙"
    
    if y_ratio < 0.33 and x_ratio < 0.33:
        position = "상단 좌측"
    elif y_ratio < 0.33 and x_ratio > 0.66:
        position = "상단 우측"
    elif y_ratio > 0.66 and x_ratio < 0.33:
        position = "하단 좌측"  
    elif y_ratio > 0.66 and x_ratio > 0.66:
        position = "하단 우측"
    elif y_ratio < 0.33 and 0.33 <= x_ratio <= 0.66:
        position = "상단 중앙"
    elif y_ratio > 0.66 and 0.33 <= x_ratio <= 0.66:
        position = "하단 중앙"
    elif 0.33 <= y_ratio <= 0.66 and x_ratio < 0.33:
        position = "중앙 좌측"
    elif 0.33 <= y_ratio <= 0.66 and x_ratio > 0.66:
        position = "중앙 우측"
    else:
        position = "중앙"
    
    
    return position

# 이전 화면 타입 저장용 전역 변수
last_screen_type = None

# 모델 불러오기 및 추론
model = YOLO("best.pt")
image_path = "test_dataset/test11.jpg" #test데이터 파일명 바꿔서 실행 가능

# 이미지 읽기 및 추론
image = cv2.imread(image_path)
img_height, img_width = image.shape[:2]
results = model(image)


# 라벨 수집
detected_labels = []
for r in results:
    for box in r.boxes:
        label = model.names[int(box.cls[0])]
        detected_labels.append(label)

# 화면 분류 및 출력
screen_type = determine_screen_type(detected_labels)
print(f"[화면 타입] {screen_type}")

# ✅ 화면이 바뀐 경우에만 멘트 출력
if screen_type != last_screen_type:
    ment_screen = screen_messages.get(screen_type)
    if ment_screen:
        speak(text=ment_screen)

        # 첫 번째 박스를 대표로 사용하여 위치 출력
        if results and results[0].boxes:
            box = results[0].boxes[0]
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            label = model.names[int(box.cls[0])]
            position = get_position_label(center_x, center_y, img_width, img_height)

            speak(position=position, label=translate_label(label))

        last_screen_type = screen_type
# ment_screen = screen_messages[screen_type]
# speak(text=ment_screen)



#메인 코드 : 라벨명, 버튼위치 받아와서 멘트 출력
for r in results:
    for box in r.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist() #바운딩박스의 양끝 좌표값
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        label = model.names[int(box.cls[0])]
        position = get_position_label(center_x, center_y, img_width, img_height)

        # # position, label만 넘겨서 tts.py에서 안내 멘트 실행
        # speak(position=position, label=translate_label(label))
