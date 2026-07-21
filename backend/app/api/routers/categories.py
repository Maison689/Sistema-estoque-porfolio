from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import CurrentUser, DbSession, require_roles
from app.models.inventory import Category
from app.models.user import UserRole
from app.schemas.inventory import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.inventory import (
    create_category,
    get_category_by_id,
    list_categories,
    update_category,
)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def read_categories(
    db: DbSession,
    _current_user: CurrentUser,
    search: str | None = None,
    is_active: bool | None = Query(default=None),
) -> list[Category]:
    return list_categories(db, search=search, is_active=is_active)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))],
)
def create_category_endpoint(payload: CategoryCreate, db: DbSession) -> Category:
    try:
        return create_category(db, payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name already exists.",
        ) from exc


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))],
)
def update_category_endpoint(
    category_id: int,
    payload: CategoryUpdate,
    db: DbSession,
) -> Category:
    category = get_category_by_id(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )
    try:
        return update_category(db, category, payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name already exists.",
        ) from exc
