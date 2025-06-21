# tts_module.py

import pyttsx3


def speak(position=None, label=None, text=None):
    if text is not None:
        ment = text
    elif position is not None and label is not None:
        ment = f"'{label}' 버튼은 {position}에 있습니다."
    
    print("[TTS] " + ment)

    engine = pyttsx3.init()
    engine.say(ment)
    engine.runAndWait()


def build_ment(position: str, label: str) -> str:
    return f"'{label}' 버튼은 {position}에 있습니다."


# 감지된 라벨 리스트로 화면 종류 유추
def determine_screen_type(labels: list) -> str:
    if "pay" in labels:
        return "결제(장바구니)화면"
    elif "membership" in labels:
        return "적립 화면"
    elif "payment_method" in labels:
        return "결제방식선택화면"
    elif "option_confirm" in labels:
        return "메뉴선택화면"
    elif "next" in labels:
        return "다음화면" 
    elif "reciept" in labels:
        return "영수증화면"
    elif "start" in labels:
        return "시작화면"

# 감지된 라벨의 한글화
def translate_label(label: str) -> str:
    translations = {
        "pay": "결제",
        "membership": "적립",
        "payment_method": "결제 방식 선택",
        "option_confirm": "메뉴 선택",
        "next": "다음",
        "reciept": "영수증",
        "start": "시작"
    }
    return translations.get(label, label)  # 기본값은 원래 라벨

# 화면별 멘트 정의
# 여기에 버튼 위치를 감지하는 기능 추가
screen_messages = {
    "결제(장바구니)화면": "메뉴를 다 고르셨다면 결제 버튼을 눌러주세요.",
    "적립 화면": "적립을 원하신다면 회원 조회 버튼을 눌러 전화번호를 입력해주세요.",
    "결제방식선택화면": "결제 방식을 선택해주세요. 카드 결제를 원하신다면 '카드 결제'버튼을 눌러주세요.",
    "메뉴선택화면": "사진을 눌러 원하는 메뉴를 선택해주세요.",
    "다음화면": "다음 화면으로 넘어가려면 '다음' 버튼을 눌러주세요.",
    "영수증화면": "영수증 출력을 원하신다면 영수증 버튼 중 '예'를 눌러주세요.",
    "시작화면": "시작 화면입니다. 원하는 방식을 눌러주세요" 
}#시작화면은 컴포즈 기준으로 멘트를 작성함
