from fastapi import APIRouter

from app.config import settings
from app.api.v1.endpoints import auth, users

api_router = APIRouter(prefix=settings.API_V1_PREFIX)
api_router.include_router(auth.router)
api_router.include_router(users.router)
