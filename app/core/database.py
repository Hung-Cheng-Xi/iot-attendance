from typing import AsyncGenerator
from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import (
	AsyncSession,
	async_sessionmaker,
	create_async_engine,
)

from app.core.settings import settings


def get_database_url() -> str:
	user = settings.postgres_user
	password = settings.postgres_password
	host = settings.postgres_host
	port = settings.postgres_port
	database = settings.postgres_db
	encoded_password = quote_plus(password)

	return f'postgresql+asyncpg://{user}:{encoded_password}@{host}:{port}/{database}'


DATABASE_URL = get_database_url()

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
	bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def create_db_session() -> AsyncSession:
	"""建立資料庫 Session 實例"""
	return async_session()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
	async with async_session() as session:
		yield session
