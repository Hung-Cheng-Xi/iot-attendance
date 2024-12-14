import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.application.schemas.configuration_schema import (
    ConfigurationInfo,
    CreateConfiguration,
)
from app.infrastructure.repositories.configuration_repository import (
    ConfigurationRepository,
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[ConfigurationInfo],
    summary="取得所有基本設定資料",
    description="取得所有基本設定資料。",
)
async def get_configurations(
    repository: Annotated[ConfigurationRepository, Depends()],
) -> List[ConfigurationInfo]:
    logging.info("取得所有 Configuration 資料")
    return await repository.get_configurations()


@router.post(
    "/",
    response_model=ConfigurationInfo,
    summary="新增基本設定",
    description="新增一筆新的基本設定資料。",
)
async def create_configuration(
    repository: Annotated[ConfigurationRepository, Depends()],
    new_configuration: CreateConfiguration,
) -> ConfigurationInfo:
    logging.info("新增一筆 Configuration 資料到資料庫")
    return await repository.create_configuration(new_configuration)
