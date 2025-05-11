from flask import Flask, request, jsonify
import openai
import base64


openai.api_key = ""
app = Flask(__name__)

@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    image = request.files["image"]
    image_bytes = image.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    vision_prompt = (
        "다음 이미지는 카페 키오스크의 화면입니다.\n"
        "이 화면의 주요 구성 요소(예: 메뉴 이름, 버튼, 안내 문구 등)를 텍스트 내용, 기능, 위치 정보와 함께 설명해 주세요.\n"
        "특히, 사용자가 눌러야 할 주요 버튼(예: 매장, 포장, 구매, 결제 등)이 어디에 있는지를 명확히 구분해 주세요.\n"
        "‘상품 준비중’처럼 선택이 불가능한 항목이 있다면 그것도 알려 주세요.\n"
        "광고, 이벤트, 앱 설치 안내 등은 중요도가 낮으면 간략히만 언급하거나 생략해도 됩니다.\n"
        "화면에 보이는 텍스트는 가능한 정확히 그대로 적어 주세요.\n"
    )

    vision_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": vision_prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{image_b64}"
                }},
            ]},
        ],
        max_tokens=1000,
    )

    parsed_result = vision_response.choices[0].message.content

    final_prompt = (
          "당신은 무인 카페 키오스크의 첫 화면을 안내하는 음성 문장을 만들어야 합니다.\n"
          "화면 하단에는 회색 '매장' 버튼과 빨간색 '포장' 버튼이 있으며, 이 둘 중 하나를 선택하는 화면입니다.\n"
          "고령자나 시각장애인이 듣고 바로 이해할 수 있도록 간단하고 명확하게 안내해야 합니다.\n\n"
          "다음 조건을 반드시 지키세요:\n"
          "- 간단한 인사를 포함하세요. 예: '안녕하세요.'\n"
          "- 그 다음 문장에서 매장에서 드시려면 왼쪽 하단의 회색 매장 버튼을 누르라고 안내하세요.\n"
          "- 그 다음 문장에서 포장하려면 오른쪽 하단의 빨간색 포장 버튼을 누르라고 안내하세요.\n"
          "- 마지막 문장에서 '다음 화면에서 메뉴를 선택하게 됩니다.'라고 알려 주세요.\n"
          "- 위 4문장 외에는 어떤 설명도 하지 마세요.\n"
          "- '오늘 픽업', '예약', '앱', '언어', '국기', '확인 버튼', '주문 완료' 등 어떤 광고나 부가 기능도 절대로 언급하지 마세요.\n"
          "- 숫자 나열(예: 1. 2. 3.)이나 목록 기호(*, → 등)도 절대 사용하지 마세요.\n"
          "- 이 네 문장을 따뜻하고 또박또박한 말투로 구성해 주세요.\n\n"
          f"화면 설명:\n{parsed_result}"
     )

    gpt_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": final_prompt}
        ],
        max_tokens=800,
    )

    tts_text = gpt_response.choices[0].message.content
    return jsonify({"tts_text": tts_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)

