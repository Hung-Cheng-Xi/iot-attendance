from datetime import date
from typing import List, Optional

from sqlmodel import SQLModel

from app.domain.models.daily_summary import WorkStatusEnum
from app.domain.models.user import User


class DailySummaryInfo(SQLModel):
	"""
	用於返回 DailySummary 的基本信息，
	適用於讀取操作。
	"""

	statistics_date: date
	total_hours: float
	status: 'WorkStatusEnum'
	overtime_hours: Optional[float]

	id: int
	user: 'User'


class PaginatedDailySummary(SQLModel):
	"""
	用於返回分頁的 DailySummary 的基本信息，
	適用於讀取操作，可返回總筆數。
	"""

	total_count: int
	items: List['DailySummaryInfo']


class CreateDailySummary(SQLModel):
	"""
	用於創建 DailySummary 記錄的 schema，
	包含需要提交的所有字段。
	"""

	statistics_date: date
	total_hours: float
	status: 'WorkStatusEnum'
	overtime_hours: Optional[float] = 0.0

	user_id: int


class UpdateDailySummary(SQLModel):
	"""
	用於更新 DailySummary 記錄的 schema，
	允許更新。
	"""

	statistics_date: date
	total_hours: float
	status: 'WorkStatusEnum'
	overtime_hours: Optional[float] = 0.0

	user_id: int
