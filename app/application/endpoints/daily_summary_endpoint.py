import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.application.schemas.daily_summary_schema import (
    CreateDailySummary,
    DailySummaryInfo,
)
from app.infrastructure.repositories.daily_summary_repository import (
    DailySummaryRepository,
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[DailySummaryInfo],
    summary="取得所有工時總結資料",
    description="取得所有工時總結資料。",
)
async def get_daily_summarys(
    repository: Annotated[DailySummaryRepository, Depends()],
) -> List[DailySummaryInfo]:
    logging.info("取得所有 DailySummary 資料")
    return await repository.get_daily_summarys()


@router.post(
    "/",
    response_model=DailySummaryInfo,
    summary="新增工時總結",
    description="新增一筆新的工時總結資料。",
)
async def create_daily_summary(
    repository: Annotated[DailySummaryRepository, Depends()],
    new_daily_summary: CreateDailySummary,
) -> DailySummaryInfo:
    logging.info("新增一筆 DailySummary 資料到資料庫")
    return await repository.create_daily_summary(new_daily_summary)
