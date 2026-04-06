# VisionScript — Multimodal Image Captioning

> **Local AI · No cloud · No API key · Powered by Ollama + LLaVA**

A sleek, dark-themed web app that generates multiple caption styles for any image using a locally-run LLaVA vision model. Upload an image, optionally add a custom question, and get instant structured captions — all running on your own machine.

---

## Preview

```
┌──────────────────────────────────────┐
│  ● VISIONSCRIPT        ollama·llava  │
│                                      │
│  DESCRIBE                            │
│  ANYTHING                            │
│                                      │
│  [ Drop image here ]                 │
│                                      │
│  ◈ One-Sentence Caption              │
│  ◉ Scene Description                 │
│  ◇ Creative / Poetic                 │
└──────────────────────────────────────┘
```

---

## Features

- **4 caption modes** — concise, detailed, creative/poetic, and custom prompt
- **Drag & drop** or click-to-upload image input (JPG, PNG, WEBP, BMP — up to 16 MB)
- **Custom questions** — ask anything about the image (e.g. *"What emotion does this convey?"*)
- **One-click copy** for each generated caption
- **Skeleton loaders** while the model is generating
- **100% local** — no data leaves your machine
- **Health endpoint** at `/health` to check Ollama status

---

## Requirements

| Requirement | Details |
|-------------|---------|
| Python | 3.8+ |
| Ollama | [https://ollama.com](https://ollama.com) |
| LLaVA model | Pulled via `ollama pull llava` |
| Python packages | `flask`, `requests`, `Pillow`, `werkzeug` |

---

## Installation

### 1. Install Ollama

Download and install from [https://ollama.com](https://ollama.com), then pull the LLaVA model:

```bash
ollama pull llava
```

> LLaVA (~4 GB) will be downloaded once and cached locally.

### 2. Clone or download this project

```
project/
├── app.py
└── static/
    └── index.html
```

Place `index.html` inside a `static/` folder next to `app.py`.

### 3. Install Python dependencies

```bash
pip install flask requests Pillow werkzeug
```

---

## Running the App

**Terminal 1 — Start Ollama:**
```bash
ollama serve
```

**Terminal 2 — Start Flask:**
```bash
python app.py
```

Then open your browser at:

```
http://localhost:5000
```

---

## Project Structure

```
project/
├── app.py              # Flask backend — handles uploads, calls Ollama API
├── static/
│   └── index.html      # Full frontend — UI, styles, JavaScript
├── uploads/            # Temporary image storage (auto-created)
└── README.md
```

---

## API Reference

### `POST /caption`

Upload an image and receive generated captions.

**Request** — `multipart/form-data`:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | file | ✅ | Image file (JPG, PNG, WEBP, BMP) |
| `prompt` | string | ❌ | Custom question about the image |

**Response** — JSON:

```json
{
  "captions": {
    "plain":    "A cat sitting on a windowsill at sunset.",
    "detail":   "The scene shows a tabby cat perched on a wooden windowsill...",
    "creative": "Silhouetted against the dying light, a small guardian watches...",
    "custom":   "The cat appears calm and contemplative."
  },
  "filename": "cat.jpg"
}
```

### `GET /health`

Returns Ollama connection status.

```json
{ "ollama": "running", "model": "llava" }
```

---

## Configuration

Edit these constants at the top of `app.py` to customize behaviour:

```python
OLLAMA_URL  = "http://localhost:11434/api/generate"   # Ollama endpoint
MODEL_NAME  = "llava"                                  # Model to use
```

To use a different model (e.g. `llava:13b` or `bakllava`):

```bash
ollama pull llava:13b
```

Then update `MODEL_NAME = "llava:13b"` in `app.py`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Ollama is not running` | Run `ollama serve` in a separate terminal |
| `ollama pull` is slow | LLaVA is ~4 GB — wait for the download to complete |
| Images render poorly | App auto-resizes to 800×800px for faster inference |
| Port 5000 in use | Change `port=5000` to another value in `app.py` |
| `ModuleNotFoundError` | Run `pip install flask requests Pillow werkzeug` |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vanilla HTML/CSS/JS — no build step |
| Backend | Python + Flask |
| Vision Model | LLaVA via Ollama |
| Image Processing | Pillow (PIL) |


---

