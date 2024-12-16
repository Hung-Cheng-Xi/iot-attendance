from datetime import date
from typing import List, Optional

from sqlmodel import SQLModel

from app.domain.models.checkin import Checkin
from app.domain.models.daily_summary import DailySummary
from app.domain.models.user import PermissionEnum


class UserInfo(SQLModel):
	name: str
	rfid: str
	position: Optional[str]
	department: Optional[str]
	hire_date: Optional[date]
	permission: "PermissionEnum"

	id: int
	checkins: List['Checkin'] = []
	daily_summaries: List['DailySummary'] = []


class CreateUser(SQLModel):
	name: str
	rfid: str = '7201-2545-6789-2490'
	position: Optional[str]
	department: Optional[str]
	hire_date: Optional[date]
	permission: "PermissionEnum"


class UpdateUser(SQLModel):
	name: str
	rfid: str
	position: Optional[str]
	department: Optional[str]
	hire_date: Optional[date]
	permission: "PermissionEnum"
