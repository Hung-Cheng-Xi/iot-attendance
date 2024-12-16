from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.domain.models.checkin import Checkin
from app.domain.models.daily_summary import DailySummary


class PermissionEnum(str, Enum):
	"""
	Attributes:
	    user: user
	    admin: admin
	"""

	user = 'user'
	admin = 'admin'


# Users 表
class User(SQLModel, table=True):
	__tablename__ = 'user'

	id: int = Field(default=None, primary_key=True)
	name: str
	rfid: str = Field(unique=True)
	position: Optional[str]  # 職位
	department: Optional[str]  # 部門
	hire_date: Optional[date]  # 入職日期
	permission: PermissionEnum = Field(
		default=PermissionEnum.user, description='權限'
	)
	created_datetime: datetime = Field(
		default_factory=lambda: datetime.now(),
		sa_column_kwargs={'server_default': 'now()'},
	)

	checkins: List['Checkin'] = Relationship(back_populates='user')  # 打卡記錄
	daily_summaries: List['DailySummary'] = Relationship(
		back_populates='user'
	)  # 每日工時總結
