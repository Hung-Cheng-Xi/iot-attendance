from typing import List

from sqlmodel import SQLModel


class ConfigurationInfo(SQLModel):
    """
    用於返回 Configuration 的基本信息，
    適用於讀取操作。
    """

    daily_min_hours: int
    overtime_rate: float

    id: int


class PaginatedConfiguration(SQLModel):
    """
    用於返回分頁的 Configuration 的基本信息，
    適用於讀取操作，可返回總筆數。
    """

    total_count: int
    items: List["ConfigurationInfo"]


class CreateConfiguration(SQLModel):
    """
    用於創建 Configuration 記錄的 schema，
    包含需要提交的所有字段。
    """

    daily_min_hours: int
    overtime_rate: float


class UpdateConfiguration(SQLModel):
    """
    用於更新 Configuration 記錄的 schema，
    允許更新。
    """

    daily_min_hours: int
    overtime_rate: float
