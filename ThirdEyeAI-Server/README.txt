[키오스크 TTS 자동화 시스템 구성]

1. Flask 서버를 실행:
   $ python flask_server.py

2. Android 앱에서 키오스크 화면 이미지를 촬영하고,
   '/analyze-image' 엔드포인트로 POST 전송 (multipart 형식)

3. 서버는 GPT-4 Vision으로 화면을 분석하고, GPT-4로 음성 설명 문장을 생성

4. 응답으로 TTS 텍스트를 Android로 전달

5. Android 앱은 TextToSpeech API를 사용해 음성 출력
