from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.domain.models.user_permission import UserPermissionLink

if TYPE_CHECKING:
    from app.domain.models.user import User


# Permissions 表
class Permission(SQLModel, table=True):
    __tablename__ = "permission"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None

    users: List["User"] = Relationship(
        link_model=UserPermissionLink,
        back_populates="permissions",
        sa_relationship_kwargs={
            "primaryjoin": "Permission.id == UserPermissionLink.permission_id",
            "secondaryjoin": "User.id == UserPermissionLink.user_id",
        },
    )
