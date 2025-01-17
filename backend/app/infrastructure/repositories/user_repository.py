from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.application.schemas.user_schema import (
	CreateUser,
	UpdateUser,
	UserInfo,
)
from app.core.database import get_db_session
from app.domain.models.user import User
from app.infrastructure.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
	def __init__(self, session: AsyncSession = Depends(get_db_session)):
		super().__init__(session)

	async def create_user(self, new_user: CreateUser) -> UserInfo:
		"""新增一個 User 到資料庫"""
		user = await self.create_instance(User(**new_user.model_dump()))
		statement = (
			select(User)
			.where(User.id == user.id)
			.options(
				selectinload(User.checkins),
				selectinload(User.daily_summaries),
			)
		)

		user = (await self.session.execute(statement)).scalars().first()

		return UserInfo.model_validate(user)

	async def get_user(self, user_id: int) -> UserInfo:
		"""根據 User ID 取得 User 資料"""
		statement = (
			select(User)
			.where(User.id == user_id)
			.options(
				selectinload(User.checkins),
				selectinload(User.daily_summaries),
			)
		)

		user = (await self.session.execute(statement)).scalars().first()
		return UserInfo.model_validate(user)

	async def get_users(self) -> List[UserInfo]:
		"""取得所有 User 資料"""
		statement = select(User).options(
			selectinload(User.checkins),
			selectinload(User.daily_summaries),
		)

		users = (await self.session.execute(statement)).scalars().all()
		return [UserInfo.model_validate(user) for user in users]

	async def update_user(
		self,
		user_id: int,
		updated_user: UpdateUser,
	) -> UserInfo:
		"""更新一筆 User 資料"""

		user_data = updated_user.model_dump()
		await self.update_instance(user_id, user_data, User)

		statement = (
			select(User)
			.where(User.id == user_id)
			.options(
				selectinload(User.checkins),
				selectinload(User.daily_summaries),
			)
		)

		users = (await self.session.execute(statement)).scalars().all()
		return [UserInfo.model_validate(user) for user in users][0]

	async def check_name_exists(self, name: str) -> bool:
		"""檢查 User 名稱是否已經存在"""
		return await self.check_exists('name', name, User)
