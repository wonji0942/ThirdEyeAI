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

## 🗂️ 데이터셋 정보

* 출처: [Roboflow - OSP Dataset v4](https://universe.roboflow.com/kiosk-nmotv/osp-bao99)

* 라이선스: CC BY 4.0

* 클래스 수: 7개
  `['membership', 'next', 'option_confirm', 'pay', 'payment_method', 'receipt', 'start']`

* 총 이미지 수: 403장
  → 직접 촬영한 원본 이미지 155장을 바탕으로 **증강 기법을 적용해 약 3배 확장**

* 라벨 포맷: YOLOv8 형식 (bounding box + class index)

* **데이터 분할**: 학습 안정성을 위해 **train/valid/test 세트로 수동 분할 구성**

* 전처리 설정:

  * 이미지 자동 방향 정렬 (Auto-Orient)
  * EXIF 메타데이터 제거
  * YOLO 입력 규격에 맞춰 \*\*640×640 해상도(Stretch 방식)\*\*로 리사이즈

* **적용된 증강 기법 (Roboflow 내 설정 기준):**

| 증강 항목           | 범위 또는 방식                      | 목적                  |
| --------------- | ----------------------------- | ------------------- |
| 회전 (Rotation)   | ±4도 이내 랜덤 회전                  | 촬영 각도 차이 대응         |
| 밝기 (Brightness) | ±20% 내 밝기 변화                  | 디스플레이 조명 환경 다양성 반영  |
| 노출 (Exposure)   | ±10% 내 광량 조절                  | 빛 반사/어두운 화면 상황 반영   |
| 노이즈 (Noise)     | 1.13% Salt & Pepper 노이즈 랜덤 삽입 | 촬영 시 카메라 노이즈 견고성 확보 |

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


## 🤝 팀원별 역할

| 이름                   | 역할                                                                                                                                                                                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **신원지(wonji0942)**   | YOLOv8 모델 증강 및 추론, 데이터셋 수집/라벨링/증강 및 분할<br>Flask 서버 및 `/analyze-image` API 설계, YOLO 추론 결과 JSON 응답 처리<br>버튼 위치 해석 및 멘트 생성, TTS 연동 및 중복 방지 로직 구현<br>Android 앱 기능 구현(CameraX 촬영, 서버 연동, OkHttp 통신)<br>서버 응답 수신 및 TextToSpeech 안내 출력<br>Zeroconf 기반 mDNS 자동 연결 구현, 전체 파이프라인 통합 테스트 및 문서 작성 |
| 양은지                  | 키오스크 데이터(사진) 직접 수집,pyttsx3를 기반으로 화면 종류에 따른 멘트를 동적으로 생성•출력하는 TTS(음성 안내) 모듈 개발 및 테스트, 로컬 환경에서 추출된 버튼 라벨명·바운딩 박스 좌표값을 기반으로 위치를 출력하는 코드 구현(main.py)                                                                                                                                                                                                                                                                              |
| 안유빈                  |키오스크 데이터(사진) 직접 수집, TTS(음성 안내) 모듈 개발                                                                                       |
| **이하영(luckygoaeng)** | YOLOv8 모델 학습 및 라벨링<br>버튼 객체 탐지 모델 개발<br>데이터 파이프라인 구축                                                                                                                                                                                                                                  |



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


---

## 📡 안드로이드 연동을 위한 서버 실행 방법

본 프로젝트는 **Flask 서버와 Android 앱 간 실시간 통신**이 가능하도록 설계되어 있습니다. Android 앱이 촬영한 이미지를 서버에 전송하면, 서버가 YOLOv8 모델로 버튼을 인식하고 **음성 안내 멘트를 JSON 형태로 응답**합니다.

### 🔹 서버 실행 순서

1. 먼저 Flask 서버를 실행합니다:

```bash
python flask_server.py
```

* 서버는 기본적으로 **6000번 포트**에서 실행되며,
* Zeroconf를 통해 `ThirdEyeKiosk._http._tcp.local.` 이름으로 **mDNS 광고**가 시작됩니다.
* 터미널에서 `[mDNS] Registered service: ThirdEyeKiosk._http._tcp.local.` 로그가 보이면 정상 실행된 것입니다.

2. Android 앱을 실행하면 앱이 자동으로 **mDNS를 통해 서버를 탐색**하고 연결을 시도합니다.

3. 앱의 촬영 버튼을 누르면, 폰 카메라로 촬영된 키오스크 화면 이미지가 Flask 서버의 `/analyze-image` API로 전송됩니다.

4. 서버는 YOLOv8 모델로 버튼을 감지하고, 감지된 버튼 라벨과 위치 정보를 바탕으로 **적절한 음성 안내 멘트 텍스트를 JSON 형태로 응답**합니다.

5. Android 앱은 해당 멘트를 수신하고, **TextToSpeech API를 통해 실시간으로 음성 안내를 출력**합니다.

---

### 📁 관련 코드 위치

| 구성 요소                | 파일 경로                                                      |
| -------------------- | ---------------------------------------------------------- |
| Flask 추론 서버 실행       | `flask_server.py`                                          |
| YOLOv8 객체 탐지 및 멘트 생성 | `YOLOv8_with_tts/main.py`, `YOLOv8_with_tts/tts_module.py` |
| Android 앱 연동 코드      | `app/src/main/java/.../MainActivity.kt`                    |

---

