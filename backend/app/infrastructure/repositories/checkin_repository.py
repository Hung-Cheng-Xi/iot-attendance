from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.application.schemas.checkin_schema import CheckinInfo
from app.core.database import get_db_session
from app.domain.models.checkin import Checkin
from app.infrastructure.repositories.base_repository import BaseRepository


class CheckinRepository(BaseRepository[Checkin]):
	def __init__(self, session: AsyncSession = Depends(get_db_session)):
		super().__init__(session)

	async def create_checkin(self, new_checkin: Checkin) -> Checkin:
		"""新增一個 Checkin 到資料庫"""
		return await self.create_instance(new_checkin)

	async def get_checkin(self, checkin_id: int) -> CheckinInfo:
		"""根據 Checkin ID 取得 Checkin 資料"""

		statement = (
			select(Checkin)
			.where(Checkin.id == checkin_id)
			.options(
				joinedload(Checkin.user),
			)
		)

		checkin = (await self.session.execute(statement)).scalar().first()
		return CheckinInfo.model_validate(checkin)

	async def get_checkins(self) -> List[CheckinInfo]:
		"""取得所有 Checkin 資料"""
		statement = select(Checkin).options(
			joinedload(Checkin.user),
		)

		checkins = (await self.session.execute(statement)).scalars().all()
		return [CheckinInfo.model_validate(checkin) for checkin in checkins]

	async def check_name_exists(self, name: str) -> bool:
		"""檢查 Checkin 名稱是否已經存在"""
		return await self.check_exists('name', name, Checkin)
