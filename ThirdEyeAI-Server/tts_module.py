import pyttsx3

# TTS 출력 함수
def speak(position=None, label=None, text=None):
    if text is not None:
        ment = text
    elif position is not None and label is not None:
        position = simplify_position(position)
        ment = f"'{label}' 버튼은 {position}에 있습니다."
    
    print("[TTS] " + ment)

    engine = pyttsx3.init()
    engine.say(ment)
    engine.runAndWait()

# TTS 멘트 문자열 생성용 함수
def build_ment(position: str, label: str) -> str:
    position = simplify_position(position)
    return f"'{label}' 버튼은 {position}에 있습니다."

# "중앙 중앙" → "중앙" 으로 정리
def simplify_position(position: str) -> str:
    return "중앙" if position.strip() == "중앙 중앙" else position.strip()

# 감지된 라벨 리스트로 화면 종류 유추
def determine_screen_type(labels: list) -> str:
    if "pay" in labels:
        return "결제(장바구니)화면"
    elif "membership" in labels:
        return "적립 화면"
    elif "payment_method" in labels:
        return "결제방식선택화면"
    elif "option_confirm" in labels:
        return "옵션선택화면"
    elif "next" in labels:
        return "다음화면" 
    elif "reciept" in labels:
        return "영수증화면"
    elif "start" in labels:
        return "시작화면"

# 감지된 라벨 → 한글 라벨 변환
def translate_label(label: str) -> str:
    translations = {
        "pay": "결제",
        "membership": "적립",
        "payment_method": "결제 방식 선택",
        "option_confirm": "옵션 선택",
        "next": "다음",
        "reciept": "영수증",
        "start": "시작"
    }
    return translations.get(label, label)

# 화면별 기본 멘트
screen_messages = {
    "결제(장바구니)화면": "메뉴를 다 고르셨다면 결제 버튼을 눌러주세요.",
    "적립 화면": "적립을 원하신다면 회원 조회 버튼을 눌러 전화번호를 입력해주세요.",
    "결제방식선택화면": "결제 방식을 선택해주세요. 카드 결제를 원하신다면 '카드 결제'버튼을 눌러주세요.",
    "옵션선택화면": "원하는 옵션을 추가한 후 '선택완료' 버튼을 눌러주세요",
    "다음화면": "다음 화면으로 넘어가려면 '다음' 버튼을 눌러주세요.",
    "영수증화면": "영수증 출력을 원하신다면 영수증 버튼 중 '예'를 눌러주세요.",
    "시작화면": "시작 화면입니다. 여기서 드실 땐 ‘매장에서 먹어요’버튼, 집에 가져가실 땐 ‘포장해서 갈래요’ 버튼을 눌러주세요."
}
