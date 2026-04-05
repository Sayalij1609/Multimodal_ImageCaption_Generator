"""
Multimodal Image Captioning — Flask Web App (Ollama + LLaVA)
Much faster startup than BLIP-2 — no model loading wait!

Requirements:
  1. Ollama installed and running  →  https://ollama.com
  2. LLaVA model pulled           →  ollama pull llava
  3. pip install flask requests Pillow werkzeug

Run:
  ollama serve          (in one terminal, if not already running)
  python app.py         (in another terminal)
  Open: http://localhost:5000
"""

import os
import base64
import requests
from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)

OLLAMA_URL  = "http://localhost:11434/api/generate"
MODEL_NAME  = "llava"

ALLOWED = {"png", "jpg", "jpeg", "webp", "bmp"}

def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

def image_to_base64(image_path):
    with Image.open(image_path).convert("RGB") as img:
        img.thumbnail((800, 800))
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode("utf-8")

def ask_llava(image_path, prompt):
    img_b64 = image_to_base64(image_path)
    payload = {
        "model":  MODEL_NAME,
        "prompt": prompt,
        "images": [img_b64],
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 100}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/caption", methods=["POST"])
def caption():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400
    file = request.files["image"]
    if not file.filename or not allowed(file.filename):
        return jsonify({"error": "Invalid file type. Use JPG, PNG, or WEBP."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    custom_prompt = request.form.get("prompt", "").strip() or None

    test = ask_llava(filepath, "Hi")
    if test is None:
        return jsonify({"error": "Ollama is not running. Start it with: ollama serve"}), 503

    captions = {
        "plain":    ask_llava(filepath, "Describe this image in one sentence. Be concise and specific."),
        "detail":   ask_llava(filepath, "What is happening in this image? Describe the scene, people, objects, and setting in 2-3 sentences."),
        "creative": ask_llava(filepath, "Write a creative and vivid caption for this image in one sentence. Make it poetic and expressive."),
        "custom":   ask_llava(filepath, custom_prompt) if custom_prompt else None,
    }

    return jsonify({"captions": captions, "filename": filename})

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/health")
def health():
    try:
        requests.get("http://localhost:11434", timeout=3)
        return jsonify({"ollama": "running", "model": MODEL_NAME})
    except:
        return jsonify({"ollama": "not running"}), 503

if __name__ == "__main__":
    print("=" * 50)
    print(f"  Model : {MODEL_NAME} via Ollama")
    print(f"  UI    : http://localhost:5000")
    print("  Make sure: ollama serve is running!")
    print("=" * 50)
    app.run(debug=False, port=5000)