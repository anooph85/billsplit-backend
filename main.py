from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

VISION_API_KEY = os.environ["VISION_API_KEY"]
VISION_URL = f"https://vision.googleapis.com/v1/images:annotate?key={VISION_API_KEY}"

@app.route("/")
def home():
    return "BillSplitBackend is running"

@app.route("/ocr-from-url", methods=["POST"])
def ocr_from_url():
    data = request.get_json()
    if not data or "image_url" not in data:
        return jsonify({"error": "image_url is required"}), 400

    image_url = data["image_url"]

    img_data = requests.get(image_url).content
    img_base64 = base64.b64encode(img_data).decode()

    body = {
        "requests": [
            {
                "image": {"content": img_base64},
                "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
            }
        ]
    }

    response = requests.post(VISION_URL, json=body).json()

    try:
        text = response["responses"][0]["fullTextAnnotation"]["text"]
    except:
        text = ""

    return jsonify({"extracted_text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
