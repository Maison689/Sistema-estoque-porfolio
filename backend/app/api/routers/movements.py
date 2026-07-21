from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import CurrentUser, DbSession, require_roles
from app.models.inventory import MovementType
from app.models.user import UserRole
from app.schemas.movement import AdjustmentCreate, MovementCreate, MovementResponse
from app.services.movements import (
    list_movements,
    register_adjustment,
    register_entry,
    register_exit,
)

router = APIRouter(prefix="/movements", tags=["movements"])
MovementTypeQuery = Query(default=None, alias="type")


@router.get("", response_model=list[MovementResponse])
def read_movements(
    db: DbSession,
    _current_user: CurrentUser,
    product_id: int | None = None,
    movement_type: MovementType | None = MovementTypeQuery,
) -> list[dict[str, object]]:
    return list_movements(db, product_id=product_id, movement_type=movement_type)


@router.post(
    "/entries",
    response_model=MovementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_entry(
    payload: MovementCreate,
    db: DbSession,
    current_user: CurrentUser,
) -> dict[str, object]:
    return register_entry(db, payload, current_user)


@router.post(
    "/exits",
    response_model=MovementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_exit(
    payload: MovementCreate,
    db: DbSession,
    current_user: CurrentUser,
) -> dict[str, object]:
    return register_exit(db, payload, current_user)


@router.post(
    "/adjustments",
    response_model=MovementResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))],
)
def create_adjustment(
    payload: AdjustmentCreate,
    db: DbSession,
    current_user: CurrentUser,
) -> dict[str, object]:
    return register_adjustment(db, payload, current_user)
