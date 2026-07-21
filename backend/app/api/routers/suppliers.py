from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import CurrentUser, DbSession, require_roles
from app.models.user import UserRole
from app.schemas.supplier import (
    ProductSupplierCreate,
    ProductSupplierResponse,
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)
from app.services.suppliers import (
    create_product_supplier,
    create_supplier,
    delete_product_supplier,
    get_supplier_by_id,
    list_product_suppliers,
    list_suppliers,
    product_supplier_to_response,
    supplier_to_response,
    update_supplier,
)

router = APIRouter(tags=["suppliers"])


@router.get("/suppliers", response_model=list[SupplierResponse])
def read_suppliers(
    db: DbSession,
    _current_user: CurrentUser,
    search: str | None = None,
    is_active: bool | None = Query(default=None),
) -> list[dict[str, object]]:
    return list_suppliers(db, search=search, is_active=is_active)


@router.post(
    "/suppliers",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))],
)
def create_supplier_endpoint(
    payload: SupplierCreate,
    db: DbSession,
) -> dict[str, object]:
    try:
        return supplier_to_response(create_supplier(db, payload))
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Supplier tax ID already exists.",
        ) from exc


@router.patch(
    "/suppliers/{supplier_id}",
    response_model=SupplierResponse,
    dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))],
)
def update_supplier_endpoint(
    supplier_id: int,
    payload: SupplierUpdate,
    db: DbSession,
) -> dict[str, object]:
    supplier = get_supplier_by_id(db, supplier_id)
    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found.",
        )
    try:
        return supplier_to_response(update_supplier(db, supplier, payload))
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Supplier tax ID already exists.",
        ) from exc


@router.get(
    "/products/{product_id}/suppliers",
    response_model=list[ProductSupplierResponse],
)
def read_product_suppliers(
    product_id: int,
    db: DbSession,
    _current_user: CurrentUser,
) -> list[dict[str, object]]:
    return list_product_suppliers(db, product_id)


@router.post(
    "/products/{product_id}/suppliers",
    response_model=ProductSupplierResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))],
)
def create_product_supplier_endpoint(
    product_id: int,
    payload: ProductSupplierCreate,
    db: DbSession,
) -> dict[str, object]:
    try:
        link = create_product_supplier(db, product_id, payload.supplier_id)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product supplier link already exists.",
        ) from exc

    supplier = get_supplier_by_id(db, payload.supplier_id)
    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found.",
        )
    return product_supplier_to_response(link, supplier)


@router.delete(
    "/products/{product_id}/suppliers/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))],
)
def delete_product_supplier_endpoint(
    product_id: int,
    supplier_id: int,
    db: DbSession,
) -> Response:
    delete_product_supplier(db, product_id, supplier_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
