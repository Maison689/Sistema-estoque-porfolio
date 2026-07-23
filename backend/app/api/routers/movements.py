from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import CurrentUser, DbSession, require_roles
from app.models.inventory import MovementType
from app.models.user import UserRole
from app.schemas.movement import (
    AdjustmentCreate,
    MovementCreate,
    MovementPage,
    MovementResponse,
)
from app.services.movements import (
    list_movements,
    register_adjustment,
    register_entry,
    register_exit,
)

router = APIRouter(prefix="/movements", tags=["movements"])
CreatedByQuery = Annotated[int | None, Query(ge=1)]
LimitQuery = Annotated[int, Query(ge=1, le=100)]
MovementTypeQuery = Annotated[MovementType | None, Query(alias="type")]
OffsetQuery = Annotated[int, Query(ge=0)]
ProductQuery = Annotated[int | None, Query(ge=1)]


@router.get("", response_model=MovementPage)
def read_movements(
    db: DbSession,
    _current_user: CurrentUser,
    product_id: ProductQuery = None,
    movement_type: MovementTypeQuery = None,
    created_by_id: CreatedByQuery = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: LimitQuery = 20,
    offset: OffsetQuery = 0,
) -> dict[str, object]:
    return list_movements(
        db,
        created_by_id=created_by_id,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        movement_type=movement_type,
        offset=offset,
        product_id=product_id,
    )


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
