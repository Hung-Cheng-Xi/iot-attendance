from sqlmodel import Field, SQLModel


class UserPermissionLink(SQLModel, table=True):
    __tablename__ = "user_permission_link"

    user_id: int = Field(foreign_key="user.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)
