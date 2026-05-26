# openorc-test

FastAPI authentication service with JWT, SQLAlchemy async, and full test coverage.

## Quick Start

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run the server
uvicorn app.main:app --reload

# Open API docs
# http://localhost:8000/docs
```

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/auth/register` | No | Register a new user |
| POST | `/api/v1/auth/login` | No | Login, returns JWT |
| POST | `/api/v1/auth/refresh` | No | Refresh JWT token |
| GET | `/api/v1/users/me` | Yes | Get current user |
| PATCH | `/api/v1/users/me` | Yes | Update current user |
| GET | `/api/v1/users/` | Admin | List all users |
| GET | `/api/v1/users/{id}` | Admin | Get user by ID |
| PATCH | `/api/v1/users/{id}` | Admin | Update any user |
| DELETE | `/api/v1/users/{id}` | Admin | Delete user |

## Testing

```bash
pytest tests/ -v --asyncio-mode=auto
```

## Tech Stack

- FastAPI
- SQLAlchemy 2.0 (async)
- JWT (python-jose)
- bcrypt (passlib)
- PostgreSQL / SQLite
- Docker
