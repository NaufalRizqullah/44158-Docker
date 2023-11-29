from fastapi import APIRouter

from src.routers.v1 import predict

router = APIRouter(prefix="/v1")

router.include_router(predict.router)