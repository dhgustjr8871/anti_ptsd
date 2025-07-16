from flask import Flask, request, jsonify
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests
import io
import base64
import torch
from flask_cors import CORS
# 한 번만 실행하면 됨
# nltk.download("punkt")
# nltk.download("stopwords")

app = Flask(__name__)
CORS(app)

# 모델과 프로세서 로드
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"💻 Using device: {device}")
model.to(device)

# 이미지 열기 함수
def load_image(data):
    if "url" in data:
        return Image.open(requests.get(data["url"], stream=True).raw).convert("RGB")
    elif "base64" in data:
        image_data = base64.b64decode(data["base64"])
        return Image.open(io.BytesIO(image_data)).convert("RGB")
    else:
        raise ValueError("No valid image source provided.")

@app.route("/blip", methods=["POST"])
def blip_caption():
    try:
        # JSON 파싱 예외 방지
        if request.is_json:
            data = request.get_json()
        else:
            return jsonify({"error": "Request is not JSON"}), 400

        image = load_image(data)
        print("✅ 이미지 shape:", image.size) 
        inputs = processor(image, return_tensors="pt").to(device)
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=20)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return jsonify({"caption": caption})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
