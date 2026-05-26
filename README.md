# FastAPI App

Simple FastAPI application.

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for interactive API documentation.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/items` | List all items |
| POST | `/api/items` | Create an item |
| GET | `/api/items/{id}` | Get item by ID |
| DELETE | `/api/items/{id}` | Delete an item |

## Testing

```bash
pip install pytest httpx
pytest tests/ -v --asyncio-mode=auto
```
