from fastapi import APIRouter

# from app.application.isms.endpoints.announcement_endpoint import (
#     router as announcement_router,
# )

main_router = APIRouter(
    prefix="/attendance",
)

# main_router.include_router(
#     minio_router,
#     prefix="/minio",
#     tags=["Minio"],
# )
