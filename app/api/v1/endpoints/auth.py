from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, decode_token
from app.schemas.token import Token
from app.schemas.user import UserCreate, LoginRequest, UserRead
from app.crud.user import user_crud

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    existing_email = await user_crud.get_by_email(db, user_in.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    existing_username = await user_crud.get_by_username(db, user_in.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )
    user = await user_crud.create(db, user_in.model_dump())
    return user


@router.post("/login", response_model=Token)
async def login(
    user_in: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await user_crud.get_by_email(db, user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    access_token = create_access_token(data={"sub": user.id})
    return Token(access_token=access_token)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token: Token,
    db: AsyncSession = Depends(get_db),
):
    payload = decode_token(token.access_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    user_id = str(payload.get("sub") or "")
    user = await user_crud.get(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )
    new_token = create_access_token(data={"sub": user.id})
    return Token(access_token=new_token)
