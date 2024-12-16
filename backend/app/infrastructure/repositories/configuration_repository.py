from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.configuration_schema import ConfigurationInfo
from app.core.database import get_db_session
from app.domain.models.configuration import Configuration
from app.infrastructure.repositories.base_repository import BaseRepository


class ConfigurationRepository(BaseRepository[Configuration]):
	def __init__(self, session: AsyncSession = Depends(get_db_session)):
		super().__init__(session)

	async def create_configuration(
		self, new_configuration: Configuration
	) -> ConfigurationInfo:
		"""新增一個 Configuration 到資料庫"""
		configuration = await self.create_instance(
			Configuration(**new_configuration.model_dump())
		)
		return ConfigurationInfo.model_validate(configuration)

	async def get_configuration(
		self, configuration_id: int
	) -> ConfigurationInfo:
		"""根據 Configuration ID 取得 Configuration 資料"""
		configuration = await self.get_by_id(configuration_id, Configuration)
		return ConfigurationInfo.model_validate(configuration)

	async def get_configurations(self) -> List[ConfigurationInfo]:
		"""取得所有 Configuration 資料"""
		configurations = await self.get_all(Configuration)
		return [
			ConfigurationInfo.model_validate(config)
			for config in configurations
		]

	async def check_name_exists(self, name: str) -> bool:
		"""檢查 Configuration 名稱是否已經存在"""
		return await self.check_exists('name', name, Configuration)
