import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.application.endpoints import main_router
from app.core.logger import configure_logging
from app.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
	logging.info('應用程式啟動')
	yield
	logging.info('應用程式關閉')


def create_app():
	configure_logging()

	app = FastAPI(
		lifespan=lifespan,
		openapi_url='/openapi.json' if settings.enable_docs else None,
		docs_url='/docs' if settings.enable_docs else None,
		redoc_url='/redoc' if settings.enable_docs else None,
	)

	app.include_router(main_router, prefix='/api')
	for route in app.routes:
		if isinstance(route, APIRoute):
			route.operation_id = route.name

	return app


app = create_app()


if __name__ == '__main__':
	import uvicorn

	uvicorn.run(
		'main:app',
		host='0.0.0.0',
		port=8000,
		log_level='debug',
		reload=True,
	)
