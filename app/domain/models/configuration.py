from sqlmodel import Field, SQLModel


# Configurations 表
class Configuration(SQLModel, table=True):
    __tablename__ = "configurations"

    id: int = Field(default=None, primary_key=True)
    daily_min_hours: int = Field(default=8)  # 每日最低工時
    overtime_rate: float = Field(default=1.5)  # 加班費比例
