from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.user_schema import (
    CreateUser,
    UpdateUser,
    UserInfo,
)
from app.core.database import get_db_session
from app.infrastructure.repositories.user_permission_repository import (
    UserPermissionRepository,
)
from app.infrastructure.repositories.user_repository import UserRepository


class UserService:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_db_session)],
        user_repository: Annotated[UserRepository, Depends()],
        user_permission_repository: Annotated[
            UserPermissionRepository, Depends()
        ],
    ):
        self.session = session
        self.user_repository = user_repository
        self.user_permission_repository = user_permission_repository

    async def create_user(self, new_user: CreateUser) -> UserInfo:
        """新增一個 User 到資料庫"""
        return await self.user_repository.create_user(new_user)

    async def update_user(
        self, user_id: int, updated_user: UpdateUser
    ) -> UserInfo:
        """更新一個 User 資料"""
        await self.user_permission_repository.update_user_permission_link(
            user_id, updated_user.permission_ids
        )
        return await self.user_repository.update_user(user_id, updated_user)
