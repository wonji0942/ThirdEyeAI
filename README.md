# 💬 키오스크 음성 안내 시스템

## 📌 프로젝트 개요
본 프로젝트는 키오스크 화면 내 버튼을 YOLOv8 모델로 실시간 인식하고,  
해당 버튼의 위치와 라벨 정보를 바탕으로 음성 안내를 제공하는 서비스입니다.

- 시각장애인, 노약자 등 디지털 취약계층을 위한 키오스크 접근성 향상
- 실시간 TTS 안내를 통해 사용자의 조작 실수 예방

---

## 🎯 주요 기능

- YOLOv8 기반 키오스크 화면 버튼 인식
- 버튼 위치 정보 계산 (상단/하단/좌측 등)
- TTS 멘트 출력 (예시 : "하단 우측에 위치한 확인 버튼을 눌러주세요")
- Flask 서버를 통한 이미지 업로드 및 응답
- 안드로이드 앱과의 연동 가능성 확보

---


---

## 🗂️ 데이터셋 정보

- 출처: [Roboflow - OSP Dataset v4](https://universe.roboflow.com/kiosk-nmotv/osp-bao99)
- 라이선스: CC BY 4.0
- 클래스 수: 7개  
  `['membership', 'next', 'option_confirm', 'pay', 'payment_method', 'receipt', 'start']`
- 총 이미지 수: 403장(원본 데이터 155장을 증강함)
- 라벨 포맷: YOLOv8 형식
- 전처리:
  - 이미지 자동 방향 정렬 및 EXIF 제거
  - 640x640 해상도로 리사이즈 (스트레치 방식)
- 증강: 각 이미지에 대해 아래 증강을 적용하여 3개의 버전 생성
  - ±4도 내 랜덤 회전
  - ±20% 내 밝기 변화
  - ±10% 내 노출 변화
  - 1.13% 픽셀에 소금-후추 노이즈 적용


---

## 📂 기능 시연

(이미지나 GIF 삽입 예정 위치)

| 기능 | 설명 |
|------|------|
| 버튼 인식 | YOLOv8 모델로 버튼 위치와 라벨 검출 |
| 위치 해석 | 화면 9분할 기준으로 상대적 위치 계산 |
| 음성 안내 | pyttsx3 모듈로 실시간 안내 멘트 출력 |

---

## 🛠️ 설치 및 실행 방법

```bash
# 1. 의존성 설치(아나콘다 가상환경)
pip install -r requirements.txt

# 2. 파일 실행
python main.py
```

---

## 🤝 팀원별 역할 (수정 필요)

| 이름 | 역할 |
|------|------|
| 신원지(wonji0942) | YOLOv8 모델 학습 및 추론<br>버튼 위치 해석 알고리즘 구현<br>TTS 연동 개발 |
| 양은지 | Flask 서버 구성<br>이미지 수신 및 JSON 응답 구현 |
| 안유빈 | 안드로이드 앱에서 이미지 전송 기능 구현<br>서버 응답 처리 및 음성 재생 |
| 이하영(luckygoaeng) | 안드로이드 앱에서 이미지 전송 기능 구현<br>서버 응답 처리 및 음성 재생 |

---

## 🔧 협업 방식 및 Git 사용 규칙

- 기능별 브랜치를 만들어 작업 후 Pull Request로 병합
- 충돌 방지를 위해 `main` 브랜치 직접 작업 금지
- README, 코드에 대한 리뷰 및 수정 요청 적극 수용
- YOLOv8 모델 학습 시, 코랩에서 각자 학습시키고 학습별 pt파일은 구글드라이브에 업로드

---

## 🧱 기술 스택

- Python 3.10
- YOLOv8 (Ultralytics)
- Flask --> 확인요망!
- OpenCV
- pyttsx3 (오프라인 TTS)
- GitHub (협업 및 버전 관리)

---

## 📜 라이선스

본 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참고하세요.

- YOLOv8 모델: Ultralytics 라이선스 ([GPL-3.0](https://github.com/ultralytics/ultralytics/blob/main/LICENSE))
- TTS 모듈 `pyttsx3`: [BSD 라이선스](https://github.com/nateshmbhat/pyttsx3/blob/master/LICENSE)
- 데이터셋: 직접 수집 및 Roboflow를 통해 전처리됨

---

## 📌 참고 사항

- 본 시스템은 실제 키오스크 UI 환경 기반으로 학습된 모델을 사용합니다.
- TTS는 pyttsx3 기반이며, gTTS로 변경 가능하도록 확장 설계되어 있습니다.


---

## ⚙️ 로컬 개발 환경 세팅 (Anaconda 사용)

본 프로젝트는 로컬에서 Python 가상환경(Anaconda)을 기반으로 실행됩니다.

### 🔹 가상환경 설치 방법

1. 아나콘다(또는 미니콘다) 설치 후, 아래 명령어로 가상환경 생성:
```bash
conda create -n KIOSK python=3.10
conda activate KIOSK
```

2. `requirements.txt` 파일을 이용해 필요한 패키지 설치:
```bash
pip install -r document/requirements.txt
```

---

## ▶️ 프로그램 실행 방법

YOLO 모델을 이용한 버튼 인식 + TTS 안내 기능을 실행하려면 아래의 파일만 실행하면 됩니다:

```bash
python YOLOv8_with_tts/main.py
```

- VSCode의 터미널이나 아나콘다 프롬프트 창에서 실행하세요.
- 실행 후, 지정된 이미지에서 버튼 인식 및 음성 안내가 자동으로 이루어집니다.
