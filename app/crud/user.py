from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.crud.base import CRUDBase
from app.core.security import hash_password


class CRUDUser(CRUDBase[User]):
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, obj_in: dict[str, Any]) -> User:
        obj_in["hashed_password"] = hash_password(obj_in.pop("password"))
        return await super().create(db, obj_in)

    async def update(
        self, db: AsyncSession, db_obj: User, obj_in: dict[str, Any]
    ) -> User:
        if "password" in obj_in and obj_in["password"] is not None:
            obj_in["hashed_password"] = hash_password(obj_in.pop("password"))
        return await super().update(db, db_obj, obj_in)


user_crud = CRUDUser(User)
