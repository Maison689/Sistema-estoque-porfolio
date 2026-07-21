from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def read_health(db: Annotated[Session, Depends(get_db)]) -> HealthResponse:
    db.execute(text("select 1"))
    settings = get_settings()
    return HealthResponse(status="ok", service=settings.app_name)
