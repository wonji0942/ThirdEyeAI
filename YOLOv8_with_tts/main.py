from ultralytics import YOLO
import cv2
from tts_module import speak, screen_messages, determine_screen_type, translate_label, build_ment

# 바운딩박스 중심 위치 → 대략적 위치 텍스트로 변환
def get_position_label(center_x, center_y, img_width, img_height):
    x_ratio = center_x / img_width
    y_ratio = center_y / img_height

    vertical = "상단" if y_ratio < 0.33 else ("중앙" if y_ratio < 0.66 else "하단")
    horizontal = "좌측" if x_ratio < 0.33 else ("중앙" if x_ratio < 0.66 else "우측")

    if vertical == "중앙" and horizontal == "중앙":
        return "중앙"
    else:
        return f"{vertical} {horizontal}"

# 모델 로드 및 이미지 경로 지정
model = YOLO("best.pt")
image_path = "test_dataset/test11.jpg"  # ← 테스트 이미지 경로 설정

# 이미지 읽기 및 전처리
image = cv2.imread(image_path)
if image is None:
    print("이미지를 불러올 수 없습니다.")
    exit()

img_height, img_width = image.shape[:2]

# (선택) 전처리: 색상 변환 및 리사이즈 (YOLO가 자동 처리하면 생략 가능)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# image = cv2.resize(image, (640, 640))

# 추론 실행
results = model(image)

# 라벨 수집
detected_labels = []
for r in results:
    for box in r.boxes:
        label = model.names[int(box.cls[0])]
        detected_labels.append(label)

# 화면 종류 판별 및 멘트 출력
screen_type = determine_screen_type(detected_labels)
ment_screen = screen_messages.get(screen_type, "화면을 인식하지 못했습니다.")
print(f"[화면 타입] {screen_type}")
speak(text=ment_screen)

# 버튼별 위치 멘트 생성 및 TTS 출력
for r in results:
    for box in r.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        label = model.names[int(box.cls[0])]
        position = get_position_label(center_x, center_y, img_width, img_height)
        ko_label = translate_label(label)

        # TTS 멘트 출력
        speak(position=position, label=ko_label)
