from typing import Optional

from sqlmodel import SQLModel


class PermissionInfo(SQLModel):
    name: str
    description: Optional[str]

    id: int


class CreatePermission(SQLModel):
    name: str
    description: Optional[str]
