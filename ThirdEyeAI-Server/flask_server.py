# server.py
# ────────────────────────────────────────────────────────────────
# • 스마트 키오스크 화면을 촬영한 이미지를 받아 YOLO(best.pt)로 UI 요소 탐지
# • tts_module의 로직을 이용해 안내 멘트(TTS용 문자열) 생성
# • Android 앱은 /analyze-image POST → {"tts_text": "..."} JSON 수신
# ────────────────────────────────────────────────────────────────

from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np

# tts_module: ① 멘트 생성 util, ② 라벨‧화면 판별 로직
from tts_module import (
    build_ment,
    determine_screen_type,
    translate_label,
    screen_messages,
)

# ────────────────────────────────────────────────────────────────
# 1) Flask 인스턴스 & YOLO 모델 (애플리케이션 시작 시 1회 로드)
# ────────────────────────────────────────────────────────────────
app = Flask(__name__)
model = YOLO("best.pt")  # 학습 완료된 모델 경로

# ────────────────────────────────────────────────────────────────
# 2) 위치(상·중·하 / 좌·중·우) 계산 함수 – main.py와 동일
# ────────────────────────────────────────────────────────────────
def get_position_label(cx: float, cy: float, w: int, h: int) -> str:
    """바운딩 박스 중심 좌표(cx, cy)를 ‘상단 좌측’ 형식의 구간 라벨로 변환"""
    x_ratio, y_ratio = cx / w, cy / h

    vertical = "상단" if y_ratio < 0.33 else ("중앙" if y_ratio < 0.66 else "하단")
    horizontal = "좌측" if x_ratio < 0.33 else ("중앙" if x_ratio < 0.66 else "우측")
    return f"{vertical} {horizontal}"

# ────────────────────────────────────────────────────────────────
# 3) /analyze-image 엔드포인트
# ────────────────────────────────────────────────────────────────
@app.route("/analyze-image", methods=["POST"])
def analyze_image() -> tuple:
    """
    클라이언트(안드로이드)가 전송한 JPEG 이미지를 분석하고
    버튼 위치 + 화면 기본 안내를 합친 멘트를 반환한다.
    """
    # 3-1) 파일 읽기 → numpy 배열 변환
    img_bytes = request.files["image"].read()
    img_np = np.frombuffer(img_bytes, np.uint8)
    image = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    if image is None:
        return jsonify({"error": "이미지를 디코딩할 수 없습니다."}), 400

    h, w = image.shape[:2]

    # 3-2) YOLO 추론
    results = model(image)

    detected_labels = []
    detailed_lines = []  # 버튼별 안내 문장 리스트

    for res in results:
        for box in res.boxes:
            cls_name = model.names[int(box.cls[0])]
            detected_labels.append(cls_name)

            # 위치 좌표 계산
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            pos_label = get_position_label(cx, cy, w, h)

            # 한글 라벨 변환 후 멘트 생성
            ko_label = translate_label(cls_name)
            detailed_lines.append(build_ment(position=pos_label, label=ko_label))

    # 3-3) 화면 타입 추론 → 기본 멘트
    screen_type = determine_screen_type(detected_labels)
    base_ment = screen_messages.get(screen_type, "화면을 확인해주세요.")

    # 3-4) 최종 TTS 텍스트(한 줄) 구성
    #     기본 멘트 + 버튼별 멘트를 공백으로 이어 붙임
    tts_text = " ".join([base_ment, *detailed_lines]).strip()

    # 3-5) JSON 응답
    return jsonify({"tts_text": tts_text})

# ────────────────────────────────────────────────────────────────
# 4) 애플리케이션 진입점
# ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 0.0.0.0:6000 → Android 단말기에서 동일 Wi-Fi IP로 접근
    app.run(host="0.0.0.0", port=6000)
