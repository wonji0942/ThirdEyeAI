# tts_module.py

import pyttsx3

def speak(position, label):
    ment = f"{position}에 위치한 {label} 버튼을 눌러주세요."
    print("[TTS] " + ment)

    engine = pyttsx3.init()
    engine.say(ment)
    engine.runAndWait()

