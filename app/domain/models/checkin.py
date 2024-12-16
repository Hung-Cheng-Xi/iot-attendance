from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
	from app.domain.models.user import User


class CheckEnum(str, Enum):
	"""
	Attributes:
	    checkin: 進入
	    checkout: 離開
	"""

	checkin = '進入'
	checkout = '離開'


# Checkins 表，記錄員工的打卡記錄
class Checkin(SQLModel, table=True):
	__tablename__ = 'checkin'

	id: int = Field(default=None, primary_key=True)
	timestamp: datetime = Field(
		default_factory=lambda: datetime.now(),
		sa_column_kwargs={'server_default': 'now()'},
	)
	type: CheckEnum = Field(default=CheckEnum.checkin, description='打卡類型')

	user_id: int = Field(foreign_key='user.id')
	user: 'User' = Relationship(back_populates='checkins')
