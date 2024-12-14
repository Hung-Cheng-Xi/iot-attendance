from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.domain.models.user import User


class WorkStatusEnum(str, Enum):
    """
    Attributes:
        normal: 標準
        early_leave: 早退
        overtime: 加班
    """

    normal = "標準"
    early_leave = "早退"
    overtime = "加班"


# DailySummaries 表，記錄員工每日的工時總結
class DailySummary(SQLModel, table=True):
    __tablename__ = "daily_summaries"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).date()
    )
    total_hours: float
    status: WorkStatusEnum = Field(
        default=WorkStatusEnum.normal, description="工作狀態"
    )
    overtime_hours: Optional[float]  # 加班時數
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    user: "User" = Relationship(back_populates="daily_summaries")
