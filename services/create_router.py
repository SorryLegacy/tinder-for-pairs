from fastapi import APIRouter
from user.routes import router as user_router


def create_routes() -> APIRouter:
    """
    Method to config all routes from app
    """
    router = APIRouter()
    router.include_router(user_router)

    return router
