from datetime import date
from typing import List, Optional

from sqlmodel import SQLModel

from app.domain.models.checkin import Checkin
from app.domain.models.daily_summary import DailySummary
from app.domain.models.permission import Permission


class UserInfo(SQLModel):
    name: str
    rfid: str
    position: Optional[str]
    department: Optional[str]
    hire_date: Optional[date]
    hourly_rate: float

    id: int
    checkins: List["Checkin"] = []
    daily_summaries: List["DailySummary"] = []
    permissions: List["Permission"] = []


class CreateUser(SQLModel):
    name: str
    rfid: str = "7201-2545-6789-2490"
    position: Optional[str]
    department: Optional[str]
    hire_date: Optional[date]
    hourly_rate: float

    # 以 List[int] 傳遞多個 permission ID
    permission_ids: List[int]


class UpdateUser(SQLModel):
    name: str
    rfid: str
    position: Optional[str]
    department: Optional[str]
    hire_date: Optional[date]
    hourly_rate: float

    # 更新時也使用 List[int] 以支持多對多關係的操作
    permission_ids: List[int]
