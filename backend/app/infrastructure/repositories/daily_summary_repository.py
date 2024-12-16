from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.application.schemas.daily_summary_schema import DailySummaryInfo
from app.core.database import get_db_session
from app.domain.models.daily_summary import DailySummary
from app.domain.models.user import User
from app.infrastructure.repositories.base_repository import BaseRepository


class DailySummaryRepository(BaseRepository[DailySummary]):
	def __init__(self, session: AsyncSession = Depends(get_db_session)):
		super().__init__(session)

	async def create_daily_summary(
		self, new_daily_summary: DailySummary
	) -> DailySummaryInfo:
		"""新增一個 DailySummary 到資料庫"""
		daily_summary = await self.create_instance(
			DailySummary(**new_daily_summary.model_dump())
		)

		user = await self.get_by_id(daily_summary.user_id, User)
		daily_summary.user = user

		return DailySummaryInfo.model_validate(daily_summary)

	async def get_daily_summary(
		self, daily_summary_id: int
	) -> DailySummaryInfo:
		"""根據 DailySummary ID 取得 DailySummary 資料"""
		statement = (
			select(DailySummary)
			.where(DailySummary.id == daily_summary_id)
			.options(
				joinedload(DailySummary.user),
			)
		)

		daily_summary = (
			(await self.session.execute(statement)).scalar().first()
		)
		return DailySummaryInfo.model_validate(daily_summary)

	async def get_daily_summarys(self) -> List[DailySummaryInfo]:
		"""取得所有 DailySummary 資料"""
		statement = select(DailySummary).options(
			joinedload(DailySummary.user),
		)

		daily_summarys = (
			(await self.session.execute(statement)).scalars().all()
		)
		return [
			DailySummaryInfo.model_validate(daily_summary)
			for daily_summary in daily_summarys
		]

	async def check_name_exists(self, name: str) -> bool:
		"""檢查 DailySummary 名稱是否已經存在"""
		return await self.check_exists('name', name, DailySummary)
