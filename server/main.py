from flask import Flask, request, jsonify
import google.generativeai as genai
import os

# Flask 서버 설정
app = Flask(__name__)

# Gemini API Key 설정 (환경변수나 직접 입력)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyA6ecOZBW_QUuPjpS_yQnY2HcYaj68yqPs")
genai.configure(api_key=GEMINI_API_KEY)

# Gemini 모델 불러오기
model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-06-17')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "No input message provided"}), 400

        response = model.generate_content(user_input)
        return jsonify({
            "response": response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
