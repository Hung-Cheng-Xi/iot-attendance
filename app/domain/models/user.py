from datetime import date, datetime, timedelta, timezone
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.domain.models.checkin import Checkin
from app.domain.models.daily_summary import DailySummary
from app.domain.models.permission import Permission
from app.domain.models.user_permission import UserPermissionLink


# Users 表
class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True)
    name: str
    rfid: str = Field(unique=True)
    position: Optional[str]  # 職位
    department: Optional[str]  # 部門
    hire_date: Optional[date]  # 入職日期
    hourly_rate: float = Field(default=0)  # 時薪
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).astimezone(
            timezone(timedelta(hours=8))
        ),
        sa_column_kwargs={"server_default": "now()"},
    )

    checkins: List["Checkin"] = Relationship(back_populates="user")  # 打卡記錄
    daily_summaries: List["DailySummary"] = Relationship(
        back_populates="user"
    )  # 每日工時總結

    permissions: List["Permission"] = Relationship(
        link_model=UserPermissionLink,
        back_populates="users",
        sa_relationship_kwargs={
            "primaryjoin": "User.id == UserPermissionLink.user_id",
            "secondaryjoin": (
                "Permission.id == UserPermissionLink.permission_id"
            ),
        },
    )
