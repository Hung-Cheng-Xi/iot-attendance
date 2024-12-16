from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.application.schemas.checkin_schema import CheckinInfo
from app.core.database import get_db_session
from app.domain.models.checkin import Checkin
from app.domain.models.user import User
from app.infrastructure.repositories.checkin_repository import (
	CheckinRepository,
)


class CheckinService:
	def __init__(
		self,
		session: Annotated[AsyncSession, Depends(get_db_session)],
		checkin_repository: Annotated[CheckinRepository, Depends()],
	):
		self.session = session
		self.checkin_repository = checkin_repository

	async def _get_rfid_user(self, rfid: str) -> User:
		statement = select(User).where(User.rfid == rfid)
		user = (await self.session.execute(statement)).scalars().first()

		if user is None:
			raise HTTPException(status_code=404, detail='RFID 尚未註冊')

		return user

	async def _get_check(self) -> str:
		statement = select(Checkin).order_by(Checkin.timestamp.desc()).limit(1)
		check = (await self.session.execute(statement)).scalars().first()

		if check is None:
			return '進入'

		if check.type == '進入':
			return '離開'

		return '進入'

	async def create_checkin(self, rfid: str) -> CheckinInfo:
		user = await self._get_rfid_user(rfid)
		type = await self._get_check()

		checkin_data = Checkin(
			**{
				'type': type,
				'user_id': user.id,
			}
		)
		checkin = await self.checkin_repository.create_instance(checkin_data)

		return CheckinInfo(**checkin.model_dump(), user=user)
