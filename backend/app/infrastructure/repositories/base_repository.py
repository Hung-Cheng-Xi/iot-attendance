from typing import Generic, List, Optional, Type, TypeVar

from fastapi import HTTPException
from sqlalchemy import desc, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

T = TypeVar('T', bound=SQLModel)


class BaseRepository(Generic[T]):
	def __init__(self, session: AsyncSession):
		self.session = session

	async def _get_total_count(self, model: Type[T], filters=None):
		"""計算符合條件的資料數量"""
		total_count_stmt = select(func.count(model.id))
		if filters:
			total_count_stmt = total_count_stmt.where(*filters)
		result = await self.session.execute(total_count_stmt)
		return result.scalar()

	def _build_filters(self, search: str, search_fields: list):
		"""建立通用的篩選條件"""
		if not search:
			return []
		return [or_(*[field.ilike(f'%{search}%') for field in search_fields])]

	def _build_paginated_query(
		self,
		model: Type[T],
		page: int,
		limit: int,
		filters=None,
		order_field=None,
	):
		"""建立通用的分頁查詢"""

		skip = (page - 1) * limit
		query = select(model).offset(skip).limit(limit)
		if filters:
			query = query.where(*filters)
		if order_field:
			query = query.order_by(desc(order_field))
		return query

	async def create_multiple(self, instances: List[T]) -> List[T]:
		"""通用的批量新增多個實例到資料庫的方法"""
		self.session.add_all(instances)
		await self.session.commit()
		return instances

	async def create_instance(self, instance: T) -> T:
		"""通用的單一新增實例到資料庫的方法"""
		self.session.add(instance)
		await self.session.commit()
		await self.session.refresh(instance)
		return instance

	async def get_by_id(self, id: int, model: Type[T]) -> Optional[T]:
		"""根據 ID 獲取實例的方法"""
		result = await self.session.get(model, id)
		return result

	async def get_all(self, model: Type[T]) -> List[T]:
		"""取得所有實例資料的方法"""
		statement = select(model)
		results = await self.session.execute(statement)
		return results.scalars().all()

	async def update_instance(
		self, id: int, new_data: dict, model: Type[T]
	) -> T:
		"""更新實例的方法"""
		instance = await self.get_by_id(id, model)
		if not instance:
			raise HTTPException(
				status_code=404,
				detail=f'找不到 ID 為 {id} 的 {model.__name__} 資料',
			)

		for key, value in new_data.items():
			setattr(instance, key, value)

		await self.session.commit()
		await self.session.refresh(instance)
		return instance

	async def delete_instance(self, id: int, model: Type[T]) -> T:
		"""刪除實例"""
		instance = await self.get_by_id(id, model)
		if not instance:
			raise HTTPException(
				status_code=404,
				detail=f'找不到 ID 為 {id} 的 {model.__name__} 資料',
			)

		await self.session.delete(instance)
		await self.session.commit()
		return instance

	async def check_exists(
		self, field_name: str, value: str, model: Type[T]
	) -> bool:
		"""通用的檢查某個欄位值是否已存在的方法"""
		statement = select(model).where(getattr(model, field_name) == value)
		result = await self.session.execute(statement)
		return result.scalars().first() is not None
