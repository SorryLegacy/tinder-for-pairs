from fastapi import APIRouter
from user.routes import router as user_router
from services.routes import router as service_router


def create_routes() -> APIRouter:  # TODO Mb refactoring
    """
    Method to config all routes from app
    """
    router = APIRouter()
    router.include_router(user_router)
    router.include_router(service_router)

    return router
