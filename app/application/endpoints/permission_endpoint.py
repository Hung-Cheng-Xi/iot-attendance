import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.application.schemas.permission_schema import (
    CreatePermission,
    PermissionInfo,
)
from app.infrastructure.repositories.permission_repository import (
    PermissionRepository,
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[PermissionInfo],
    summary="取得所有權限資料",
    description="取得所有權限資料。",
)
async def get_permissions(
    repository: Annotated[PermissionRepository, Depends()],
) -> List[PermissionInfo]:
    logging.info("取得所有 Permission 資料")
    return await repository.get_permissions()


@router.post(
    "/",
    response_model=PermissionInfo,
    summary="新增權限",
    description="新增一筆新的權限資料。",
)
async def create_permission(
    repository: Annotated[PermissionRepository, Depends()],
    new_permission: CreatePermission,
) -> PermissionInfo:
    logging.info("新增一筆 Permission 資料到資料庫")
    return await repository.create_permission(new_permission)
