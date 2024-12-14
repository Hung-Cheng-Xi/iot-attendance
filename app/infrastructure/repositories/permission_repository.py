from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.permission_schema import (
    CreatePermission,
    PermissionInfo,
)
from app.core.database import get_db_session
from app.domain.models.permission import Permission
from app.infrastructure.repositories.base_repository import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        super().__init__(session)

    async def create_permission(
        self, new_permission: CreatePermission
    ) -> PermissionInfo:
        """新增一個 Permission 到資料庫"""
        permission = await self.create_instance(
            Permission(**new_permission.model_dump())
        )
        return PermissionInfo.model_validate(permission)

    async def get_permission(self, permission_id: int) -> PermissionInfo:
        """根據 Permission ID 取得 Permission 資料"""
        permission = await self.get_by_id(permission_id, Permission)
        return PermissionInfo.model_validate(permission)

    async def get_permissions(self) -> List[PermissionInfo]:
        """取得所有 Permission 資料"""
        permissions = await self.get_all(Permission)
        return [
            PermissionInfo.model_validate(permission)
            for permission in permissions
        ]

    async def check_name_exists(self, name: str) -> bool:
        """檢查 Permission 名稱是否已經存在"""
        return await self.check_exists("name", name, Permission)
