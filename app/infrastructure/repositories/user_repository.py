from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.application.schemas.user_schema import CreateUser, UserInfo
from app.core.database import get_db_session
from app.domain.models.permission import Permission
from app.domain.models.user import User
from app.infrastructure.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        super().__init__(session)

    async def fetch_permissions(
        self, permission_ids: List[int]
    ) -> List[Permission]:
        # 批量查詢 Permissions，減少資料庫請求次數
        permissions = (
            (
                await self.session.execute(
                    select(Permission).where(Permission.id.in_(permission_ids))
                )
            )
            .scalars()
            .all()
        )

        return permissions

    async def create_user(self, new_user: CreateUser) -> UserInfo:
        """新增一個 User 到資料庫"""
        permissions = await self.fetch_permissions(new_user.permission_ids)
        new_user_data = {
            **new_user.model_dump(),
            "permissions": permissions,
        }

        new_user = User(**new_user_data)
        user = await self.create_instance(new_user)

        return UserInfo(
            **user.model_dump(),
            permissions=permissions,
        )

    async def get_user(self, user_id: int) -> UserInfo:
        """根據 User ID 取得 User 資料"""
        statement = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.permissions),
                selectinload(User.checkins),
                selectinload(User.daily_summaries),
            )
        )

        user = (await self.session.execute(statement)).scalars().first()
        return UserInfo.model_validate(user)

    async def get_users(self) -> List[UserInfo]:
        """取得所有 User 資料"""
        statement = select(User).options(
            selectinload(User.permissions),
            selectinload(User.checkins),
            selectinload(User.daily_summaries),
        )

        users = (await self.session.execute(statement)).scalars().all()
        return [UserInfo.model_validate(user) for user in users]

    async def update_user(
        self,
        user_id: int,
        updated_user: User,
    ) -> UserInfo:
        """更新一筆 User 資料"""

        user_data = updated_user.model_dump()
        user_data.pop("permission_ids")

        await self.update_instance(user_id, user_data, User)

        statement = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.permissions),
                selectinload(User.checkins),
                selectinload(User.daily_summaries),
            )
        )

        users = (await self.session.execute(statement)).scalars().all()
        return [UserInfo.model_validate(user) for user in users][0]

    async def check_name_exists(self, name: str) -> bool:
        """檢查 User 名稱是否已經存在"""
        return await self.check_exists("name", name, User)
