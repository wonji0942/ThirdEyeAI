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
        "다음 이미지는 키오스크의 화면입니다.\n"
        "이 화면에서 버튼, 텍스트, 메뉴 구성과 가격 등의 요소를 위치 정보와 함께 설명해 주세요.\n"
        "각 항목에 대해 '텍스트 내용', '화면 위치', '기능'을 알려 주세요."
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
        "다음은 카페 키오스크의 화면입니다.\n\n"
        "이 화면을 처음 보는 고령자, 시각장애인, 치매 환자분들이 쉽게 이해할 수 있도록 음성 안내 문장을 만들어 주세요.\n\n"
        "조건:\n"
        "1. 쉬운 단어만 사용하세요.\n"
        "2. 문장은 짧게 써 주세요.\n"
        "3. 버튼의 위치와 기능을 설명해 주세요.\n"
        "4. 가격은 천 단위로 끊어 주세요.\n"
        "5. 마지막엔 무엇을 누르면 되는지 알려 주세요.\n"
        "6. 친절한 말투로 설명해 주세요.\n\n"
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
    app.run(host="0.0.0.0", port=5000)

