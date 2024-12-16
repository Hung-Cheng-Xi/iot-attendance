from datetime import datetime
from typing import List

from sqlmodel import SQLModel

from app.domain.models.checkin import CheckEnum
from app.domain.models.user import User


class CheckinInfo(SQLModel):
	"""
	用於返回 Checkin 的基本信息，
	適用於讀取操作。
	"""

	timestamp: datetime
	type: 'CheckEnum'

	id: int
	user: 'User'


class PaginatedCheckin(SQLModel):
	"""
	用於返回分頁的 Checkin 的基本信息，
	適用於讀取操作，可返回總筆數。
	"""

	total_count: int
	items: List['CheckinInfo']


class CreateCheckin(SQLModel):
	"""
	用於創建 Checkin 記錄的 schema，
	包含需要提交的所有字段。
	"""

	type: 'CheckEnum'

	user_id: int
