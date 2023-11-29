from fastapi import APIRouter
from src.routers.v1 import wrapper_v1

main_api = APIRouter()

main_api.include_router(wrapper_v1.router)