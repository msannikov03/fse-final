# Project Service (Skeleton)

Inital skeleton. It includes:

- Python build system (`pyproject.toml`)
- App server (FastAPI)
- Unit tests (pytest)
- Dockerfile for containerized runs
- GitHub Actions CI on every push (install → test → docker build)

---

## Architecture

- **`app/main.py`**: A tiny FastAPI app exposing one GET endpoint (`/`) and one POST endpoint (`/api`).
- **`tests/test_api.py`**: Smoke tests for both endpoints.
- **`pyproject.toml`**: Build tool + dependencies.
- **`Dockerfile`**: Production-like container (Python 3.11, uvicorn).
- **`.github/workflows/ci.yml`**: CI on every push and pull request.

---

## Quickstart (local)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest -q
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
