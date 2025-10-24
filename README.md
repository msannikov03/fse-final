# Sentiment Analysis Service

AI-powered sentiment analysis web service using DistilBERT and FastAPI.

## Features

- 🤖 **Pre-trained AI Model**: DistilBERT fine-tuned for sentiment analysis
- 💡 **Lightweight**: ~67MB model optimized for CPU (perfect for laptops)
- 🎨 **Modern Web UI**: Beautiful gradient interface with real-time analysis
- 🚀 **FastAPI Backend**: High-performance async API with Jinja2 templates
- ✅ **Unit Tests**: Comprehensive pytest coverage (6 tests)
- 🐳 **Docker Ready**: Containerized deployment
- 🔄 **CI/CD**: GitHub Actions automation with linting (black, ruff, isort, flake8)

---

## AI Model

**Model**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Size**: ~67MB (lightweight!)
- **Type**: Transformer-based sentiment classifier
- **Output**: POSITIVE or NEGATIVE with confidence scores
- **Hardware**: Runs on CPU (device=-1), no GPU required
- **Speed**: Fast inference on laptops

---

## Architecture

```
app/
├── main.py              # FastAPI backend with DistilBERT
├── templates/
│   └── index.html       # Frontend UI
└── static/              # Static assets
```

**Endpoints:**
- `GET /` - Web UI for sentiment analysis
- `GET /health` - Health check endpoint
- `POST /api/sentiment` - Sentiment analysis API (accepts JSON)

**Other files:**
- **`tests/test_api.py`**: 6 comprehensive tests
- **`pyproject.toml`**: Dependencies (FastAPI, transformers, torch)
- **`Dockerfile`**: Production container (Python 3.11, uvicorn)
- **`.github/workflows/ci.yml`**: CI pipeline

---

## Quickstart (local)

```bash
# Install dependencies (without venv)
pip3 install --break-system-packages -e .

# Run tests
python3 -m pytest -v

# Start server
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then open in your browser: **http://localhost:8000**

**Note**: On first run, the DistilBERT model (~67MB) will be downloaded automatically from HuggingFace.

---

## Using the Web UI

1. Open **http://localhost:8000** in your browser
2. Enter or paste your text in the textarea
3. Click **"Analyze Sentiment"**
4. View the AI analysis:
   - Sentiment label (POSITIVE/NEGATIVE)
   - Confidence score
   - Detailed score breakdown

---

## API Usage

### Via curl:
```bash
# Health check
curl http://localhost:8000/health

# Analyze positive text
curl -X POST http://localhost:8000/api/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text":"I love this product! It works great and exceeded my expectations."}'

# Response example:
# {
#   "label": "POSITIVE",
#   "confidence": 0.9998,
#   "scores": {
#     "POSITIVE": 0.9998,
#     "NEGATIVE": 0.0002
#   }
# }
```

### Analyze negative text:
```bash
curl -X POST http://localhost:8000/api/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text":"This is terrible and disappointing. Waste of money."}'

# Response example:
# {
#   "label": "NEGATIVE",
#   "confidence": 0.9995,
#   "scores": {
#     "POSITIVE": 0.0005,
#     "NEGATIVE": 0.9995
#   }
# }
```

---

## Development

### Linting & Formatting
```bash
# Format code
black app/ tests/
isort app/ tests/

# Check code quality
ruff check app/ tests/
flake8 app/ tests/ --max-line-length=100 --extend-ignore=E203,W503

# Run all checks
isort --check-only app/ tests/
black --check app/ tests/
ruff check app/ tests/
pytest -v
```

### Code Quality Tools
- **black**: Code formatting
- **isort**: Import sorting
- **ruff**: Fast linting
- **flake8**: PEP 8 compliance

---

## Docker

```bash
docker build -t sentiment-service .
docker run -p 8000:8000 sentiment-service
```

---

## Technology Stack

- **FastAPI**: Modern async web framework
- **HuggingFace Transformers**: Pre-trained DistilBERT model
- **PyTorch**: Deep learning framework
- **Jinja2**: Template engine
- **Pytest**: Testing framework
- **Uvicorn**: ASGI server

---

## Performance

- **Model size**: ~67MB
- **Inference time**: ~50-200ms on CPU (depending on text length)
- **Memory usage**: ~500MB RAM
- **Platform**: Works on any laptop with Python 3.11+

Perfect for development, testing, and small-scale production deployments!
