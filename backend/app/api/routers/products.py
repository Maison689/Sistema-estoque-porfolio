from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import CurrentUser, DbSession, require_roles
from app.models.user import UserRole
from app.schemas.inventory import ProductCreate, ProductResponse, ProductUpdate
from app.services.inventory import (
    create_product,
    get_product_by_id,
    list_products,
    product_to_response,
    update_product,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
def read_products(
    db: DbSession,
    _current_user: CurrentUser,
    search: str | None = None,
    category_id: int | None = None,
    is_active: bool | None = Query(default=None),
    stock_status: str | None = Query(default=None),
) -> list[dict[str, object]]:
    return list_products(
        db,
        search=search,
        category_id=category_id,
        is_active=is_active,
        stock_status=stock_status,
    )


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))],
)
def create_product_endpoint(payload: ProductCreate, db: DbSession) -> dict[str, object]:
    try:
        product = create_product(db, payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product SKU already exists.",
        ) from exc

    return product_to_response(product)


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))],
)
def update_product_endpoint(
    product_id: int,
    payload: ProductUpdate,
    db: DbSession,
) -> dict[str, object]:
    product = get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    try:
        return product_to_response(update_product(db, product, payload))
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product SKU already exists.",
        ) from exc
