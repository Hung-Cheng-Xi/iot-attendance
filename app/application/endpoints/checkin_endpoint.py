import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.application.schemas.checkin_schema import CheckinInfo
from app.domain.services.checkin_service import CheckinService
from app.infrastructure.repositories.checkin_repository import (
	CheckinRepository,
)

router = APIRouter()


@router.get(
	'/',
	response_model=List[CheckinInfo],
	summary='取得所有打卡紀錄資料',
	description='取得所有打卡紀錄資料。',
)
async def get_checkins(
	repository: Annotated[CheckinRepository, Depends()],
) -> List[CheckinInfo]:
	logging.info('取得所有 Checkin 資料')
	return await repository.get_checkins()


@router.post(
	'/',
	response_model=CheckinInfo,
	summary='新增打卡紀錄',
	description='新增一筆新的打卡紀錄資料。',
)
async def create_checkin(
	service: Annotated[CheckinService, Depends()],
	rfid: str,
) -> CheckinInfo:
	logging.info('新增一筆 Checkin 資料到資料庫')
	return await service.create_checkin(rfid)
