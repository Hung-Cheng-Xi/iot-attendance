from typing import Annotated, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_db_session
from app.domain.models.user_permission import UserPermissionLink
from app.infrastructure.repositories.base_repository import BaseRepository
from app.infrastructure.repositories.user_repository import UserRepository


class UserPermissionRepository(BaseRepository[UserPermissionLink]):
    def __init__(
        self,
        user_repository: Annotated[UserRepository, Depends()],
        session: AsyncSession = Depends(get_db_session),
    ):
        super().__init__(session)
        self.user_repository = user_repository

    async def update_user_permission_link(
        self, user_id: int, permission_ids: List[int]
    ) -> None:
        """更新一個 UserPermission 到資料庫"""

        user = await self.user_repository.get_user(user_id)
        existing_links = user.permissions

        # 獲取使用者現有的 UserPermissionLink 記錄
        existing_permission_ids = {link.id for link in existing_links}

        # 計算要新增的權限 ID 和要刪除的權限 ID
        new_permission_ids = set(permission_ids)
        permissions_to_add = new_permission_ids - existing_permission_ids
        permissions_to_remove = existing_permission_ids - new_permission_ids

        # 新增新的 UserPermissionLink 記錄
        if permissions_to_add:
            new_links = []
            for permission_id in permissions_to_add:
                new_links.append(
                    UserPermissionLink(
                        user_id=user_id, permission_id=permission_id
                    )
                )

            await self.create_multiple(new_links)

        # 刪除多餘的 UserPermissionLink 記錄
        if permissions_to_remove:
            statement = select(UserPermissionLink).where(
                UserPermissionLink.user_id == user_id,
                UserPermissionLink.permission_id.in_(permissions_to_remove),
            )

            links_to_remove = (
                (await self.session.execute(statement)).scalars().all()
            )
            for link in links_to_remove:
                await self.session.delete(link)

            self.session.commit()
