from fastapi import APIRouter

from src.api.routes import info


def create_root_router() -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(info.router)

    return api_router
