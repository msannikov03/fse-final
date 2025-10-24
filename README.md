# Sentiment Analysis Service

A lightweight sentiment analysis web service powered by FastAPI and HuggingFace Transformers.

## Features

- **Sentiment Analysis API**: Analyzes text sentiment (positive/negative) using DistilBERT
- **Lightweight Model**: ~67MB DistilBERT model optimized for CPU (perfect for laptops)
- **Production Ready**: FastAPI, pytest, Docker, GitHub Actions CI
- **Easy to Use**: Simple REST API with JSON input/output

---

## Architecture

- **`app/main.py`**: FastAPI app with sentiment analysis endpoint using `distilbert-base-uncased-finetuned-sst-2-english`
- **`tests/test_api.py`**: Comprehensive tests for sentiment analysis
- **`pyproject.toml`**: Build tool + dependencies (FastAPI, transformers, torch)
- **`Dockerfile`**: Production-ready container (Python 3.11, uvicorn)
- **`.github/workflows/ci.yml`**: CI pipeline with linting, testing, and Docker build

---

## Quickstart (local)

```bash
# Create virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Run tests
pytest -q

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Usage

### Check service status
```bash
curl http://localhost:8000/
```

### Analyze sentiment
```bash
curl -X POST http://localhost:8000/api/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product! It works great!"}'
```

**Response:**
```json
{
  "tag": "POSITIVE",
  "scores": [0.9998, 0.0002]
}
```

- `tag`: `POSITIVE` or `NEGATIVE`
- `scores`: `[positive_score, negative_score]`

---

## Docker

```bash
docker build -t sentiment-service .
docker run -p 8000:8000 sentiment-service
```

---

## CI/CD Pipeline

The CI pipeline runs on every push and pull request:

1. **Lint & Format**: Code quality checks with Ruff, Black, and isort
2. **Tests**: pytest with coverage on Python 3.11 & 3.12
3. **Docker Build**: Builds and tests the Docker container

### Development

```bash
# Install with dev dependencies for linting
pip install -e ".[dev]"

# Format code
black app/ tests/
isort app/ tests/

# Check linting
ruff check app/ tests/
black --check app/ tests/
isort --check-only app/ tests/

# Run tests with coverage
pytest --cov=app --cov-report=html -v
```
