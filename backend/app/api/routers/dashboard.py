from fastapi import APIRouter, Depends

from app.api.dependencies import DbSession, require_roles
from app.models.user import UserRole
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard import get_dashboard

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))],
)


@router.get("", response_model=DashboardResponse)
def read_dashboard(db: DbSession) -> dict[str, object]:
    return get_dashboard(db)
