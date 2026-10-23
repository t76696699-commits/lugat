import os
import time
from flask import Flask, jsonify, render_template, request
import google.generativeai as genai

app = Flask(__name__)


API_KEY = "AQ.Ab8RN6Lj0xcgHROsXTdfTm1Xpug2zuqZ6t-Cb5WgVyCTig0Anw"


genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3.5-flash-lite')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/translate-text', methods=['POST'])
def translate_text():
    data = request.get_json() or {}
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "Matn kiritilmadi"}), 400

    prompt = f"Sen professional tarjimonsan. Quyidagi matnni o'zbek tiliga tushunarli, ravon va adabiy qilib tarjima qil:\n\n{text}"

    try:
        response = model.generate_content(prompt)
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": f"Xatolik yuz berdi: {str(e)}"}), 500


@app.route('/api/translate-image', methods=['POST'])
def translate_image():
    if 'image' not in request.files:
        return jsonify({"error": "Rasm yuklanmadi"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Fayl tanlanmadi"}), 400

    try:
        image_bytes = file.read()
        image_part = {
            "mime_type": file.content_type or "image/jpeg",
            "data": image_bytes
        }

        prompt = (
            "Ushbu rasmdagi barcha matnlarni (qaysi tilda bo'lishidan qat'i nazar) aniqlagan holda "
            "o'qib chiq va uni to'liq o'zbek tiliga tarjima qilib ber. "
            "Javobda avval aniqlangan matnni, keyin esa uning o'zbekcha tarjimasini aniq qilib yoz."
        )

        response = model.generate_content([image_part, prompt])
        return jsonify({"result": response.text})

    except Exception as e:
        return jsonify({"error": f"Rasmni qayta ishlashda xatolik: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)