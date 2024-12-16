import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.application.schemas.user_schema import (
	CreateUser,
	UpdateUser,
	UserInfo,
)
from app.infrastructure.repositories.user_repository import UserRepository

router = APIRouter()


@router.get(
	'/',
	response_model=List[UserInfo],
	summary='取得所有用戶資料',
	description='取得所有用戶資料。',
)
async def get_users(
	repository: Annotated[UserRepository, Depends()],
) -> List[UserInfo]:
	logging.info('取得所有 User 資料')
	return await repository.get_users()


@router.post(
	'/',
	response_model=UserInfo,
	summary='新增用戶',
	description='新增一筆新的用戶資料。',
)
async def create_user(
	repository: Annotated[UserRepository, Depends()],
	new_user: CreateUser,
) -> UserInfo:
	logging.info('新增一筆 User 資料到資料庫')

	return await repository.create_user(new_user)


@router.get(
	'/{user_id}',
	response_model=UserInfo,
	summary='取得用戶資料',
	description='根據用戶 ID 取得用戶資料。',
)
async def get_user(
	user_id: int,
	repository: Annotated[UserRepository, Depends()],
) -> UserInfo:
	logging.info('取得 User 資料')
	return await repository.get_user(user_id)


@router.put(
	'/{user_id}',
	response_model=UserInfo,
	summary='更新用戶資料',
	description='更新指定 ID 的用戶資料。',
)
async def update_user(
	user_id: int,
	updated_user: UpdateUser,
	repository: Annotated[UserRepository, Depends()],
) -> UserInfo:
	logging.info('更新 User 資料')
	return await repository.update_user(user_id, updated_user)
