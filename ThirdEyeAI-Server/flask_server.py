from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np

# mDNS 서비스 광고를 위한 zeroconf
from zeroconf import Zeroconf, ServiceInfo
import socket
import atexit

# tts_module: 멘트 생성 및 라벨/화면 판별 로직
from tts_module import (
    build_ment,
    determine_screen_type,
    translate_label,
    screen_messages,
)

# Flask 인스턴스
app = Flask(__name__)

# ────────────────────────────────────────────────────────────────
# mDNS 서비스 등록 (zeroconf)
zeroconf = Zeroconf()
service_name = "ThirdEyeKiosk._http._tcp.local."
info = ServiceInfo(
    "_http._tcp.local.",                      # 서비스 타입
    service_name,                               # 서비스 이름
    addresses=[socket.inet_aton("192.168.1.99")],  # 실제 서버 IP
    port=6000,                                   # Flask 포트
    properties={"path": "/analyze-image"},
    server="thirdeyekiosk.local."
)
zeroconf.register_service(info)
print(f"[mDNS] Registered service: {service_name}")

# 애플리케이션 종료 시 mDNS 서비스 해제
def cleanup_mdns():
    zeroconf.unregister_service(info)
    zeroconf.close()
    print("[mDNS] Unregistered service")

atexit.register(cleanup_mdns)
# ────────────────────────────────────────────────────────────────

# YOLO 모델 로드 (애플리케이션 시작 시 1회)
model = YOLO("best.pt")  # 학습 완료된 weight 파일 경로

# 위치(상·중·하 / 좌·중·우) 계산 함수
def get_position_label(cx: float, cy: float, w: int, h: int) -> str:
    x_ratio, y_ratio = cx / w, cy / h
    vertical = "상단" if y_ratio < 0.33 else ("중앙" if y_ratio < 0.66 else "하단")
    horizontal = "좌측" if x_ratio < 0.33 else ("중앙" if x_ratio < 0.66 else "우측")
    return f"{vertical} {horizontal}"

# /analyze-image 엔드포인트
@app.route("/analyze-image", methods=["POST"])
def analyze_image() -> tuple:
    # 1) 파일 존재 확인
    if "image" not in request.files:
        return jsonify({"error": "이미지 파일 파라미터가 없습니다."}), 400

    # 2) 이미지 읽기 및 디코딩
    img_bytes = request.files["image"].read()
    img_np = np.frombuffer(img_bytes, np.uint8)
    image = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    if image is None:
        return jsonify({"error": "이미지를 디코딩할 수 없습니다."}), 400

    h, w = image.shape[:2]

    # 3) YOLO 추론
    results = model(image)

    detected_labels = []
    detailed_lines = []  # 버튼별 안내문 리스트

    for res in results:
        for box in res.boxes:
            cls_name = model.names[int(box.cls[0])]
            detected_labels.append(cls_name)

            # 박스 중심 좌표 계산
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            pos_label = get_position_label(cx, cy, w, h)

            # 한글 라벨 변환 후 멘트 생성
            ko_label = translate_label(cls_name)
            detailed_lines.append(build_ment(position=pos_label, label=ko_label))

    # 4) 화면 타입 추론 → 기본 멘트
    screen_type = determine_screen_type(detected_labels)
    base_ment = screen_messages.get(screen_type, "화면을 확인해주세요.")

    # 5) 최종 TTS 텍스트 구성
    tts_text = " ".join([base_ment, *detailed_lines]).strip()
    return jsonify({"tts_text": tts_text})

# 애플리케이션 진입점
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)

