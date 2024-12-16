from fastapi import APIRouter

from app.application.endpoints.checkin_endpoint import router as checkin_router
from app.application.endpoints.configuration_endpoint import (
	router as configuration_router,
)
from app.application.endpoints.daily_summary_endpoint import (
	router as daily_summary_router,
)
from app.application.endpoints.user_endpoint import router as user_router

main_router = APIRouter(
	prefix='/attendance',
)

main_router.include_router(
	checkin_router,
	prefix='/checkin',
	tags=['Checkin'],
)

main_router.include_router(
	user_router,
	prefix='/user',
	tags=['User'],
)

main_router.include_router(
	configuration_router,
	prefix='/configuration',
	tags=['Configuration'],
)

main_router.include_router(
	daily_summary_router,
	prefix='/daily_summary',
	tags=['DailySummary'],
)
