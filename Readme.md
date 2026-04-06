# VisionCap — CNN + LSTM Image Captioning

A multimodal image captioning system built from scratch using a ResNet50 CNN encoder and LSTM decoder, trained on the Flickr8k dataset.

---

## Project Structure

```
Multimodal_captioning_1/
├── train.py                  ← Train the model on Flickr8k
├── app.py                    ← Flask web server (run this for the UI)
├── predict.py                ← Caption a single image from terminal
├── requirements.txt          ← Python dependencies
├── model_checkpoint.pth      ← Saved after training (auto-generated)
├── vocab.pkl                 ← Vocabulary saved after training (auto-generated)
├── static/
│   └── index.html            ← Web UI
├── uploads/                  ← Uploaded images stored here (auto-created)
└── flickr8k/
    ├── Images/               ← 8,000 .jpg image files
    └── captions.txt          ← CSV with columns: image, caption
```

---

## Setup

### 1. Install dependencies

```bash
pip install torch torchvision flask Pillow werkzeug pandas numpy nltk
```

### 2. Download Flickr8k dataset

Download from Kaggle: https://www.kaggle.com/datasets/adityajn105/flickr8k

Unzip and place it so the structure matches:
```
flickr8k/
  Images/       ← all .jpg files here
  captions.txt  ← CSV file here
```

---

## Usage

### Step 1 — Train the model

```bash
python train.py
```

This trains the CNN + LSTM model and saves:
- `model_checkpoint.pth` — best model weights
- `vocab.pkl` — learned vocabulary

**Training config** (edit at top of `train.py`):

| Setting | Default | Description |
|---|---|---|
| `NUM_IMAGES` | `1000` | Number of images to train on (`None` = all 8000) |
| `EPOCHS` | `15` | Number of training epochs |
| `BATCH_SIZE` | `16` | Images per batch |
| `EMBED_DIM` | `256` | Feature vector size |
| `HIDDEN_DIM` | `512` | LSTM hidden state size |

**Estimated training time:**

| Images | GPU (RTX 30xx) | CPU |
|---|---|---|
| 1000 | ~4–6 min | ~15–20 min |
| 2000 | ~8–12 min | ~30–40 min |
| 8000 | ~30–45 min | ~3–4 hrs |

---

### Step 2 — Run the web UI

```bash
python app.py
```

Open in browser: **http://localhost:5000**

Upload any image using drag & drop or the file picker. The model generates a caption instantly.

---

### Caption a single image from terminal

```bash
python predict.py --image path/to/image.jpg
```

---

## Model Architecture

```
Image (224×224)
    │
    ▼
ResNet50 (pretrained on ImageNet)
    │  Last FC replaced with Linear(2048 → 256)
    ▼
Feature Vector (256-dim)
    │
    ▼
LSTM Decoder
    │  Embedding(vocab_size, 256) → LSTM(256, 512) → Linear(512, vocab_size)
    ▼
Beam Search (k=3)
    │
    ▼
Caption text
```

### Key design choices

- **ResNet50 encoder** — pretrained on ImageNet, only the last block and FC layer are fine-tuned
- **LSTM decoder** — learns to generate words conditioned on the image feature
- **Teacher forcing** — during training, ground truth tokens are fed as input at each step
- **Beam search** — at inference, keeps top-3 candidate sequences and picks the best
- **CrossEntropyLoss** — ignores `<PAD>` tokens, so variable-length captions train cleanly

---

## Evaluation

After training, BLEU scores are printed automatically:

```
BLEU-1: 0.38    ← word-level overlap with human captions
BLEU-4: 0.12    ← 4-gram phrase overlap (stricter)
```

Higher is better. BLEU-1 above 0.35 on 1000 images is expected and acceptable.

---

## Dependencies

| Package | Purpose |
|---|---|
| `torch` + `torchvision` | Model training and ResNet50 |
| `flask` | Web server for the UI |
| `Pillow` | Image loading and resizing |
| `nltk` | BLEU score tokenization |
| `pandas` | Reading captions.txt |
| `numpy` | Dataset shuffling |
| `werkzeug` | Secure file uploads |

---

## GPU Setup (recommended)

Check if PyTorch detects your GPU:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

If it prints `False`, reinstall PyTorch with CUDA:
```bash
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```