from services.schemas import ServiceHealthCheck
from services.database import db_depends

from fastapi import APIRouter
from sqlalchemy import select

router = APIRouter()


@router.get(
    "/healtcheck",
    summary="Healthcheck service and database",
    response_model=ServiceHealthCheck,
)
async def healthcheck(db: db_depends) -> ServiceHealthCheck:
    """
    HealthCheck endpoint
    """
    try:
        db.execute(select(1)).scalar()
    except Exception:
        return ServiceHealthCheck(service="OK", database="Error")
    else:
        return ServiceHealthCheck(service="OK", database="OK")
