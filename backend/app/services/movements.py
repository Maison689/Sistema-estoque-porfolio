from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.inventory import InventoryBalance, MovementType, Product, StockMovement
from app.models.user import User
from app.schemas.movement import AdjustmentCreate, MovementCreate


def register_entry(
    db: Session,
    payload: MovementCreate,
    current_user: User,
) -> dict[str, object]:
    return register_movement(
        db,
        product_id=payload.product_id,
        movement_type=MovementType.ENTRY,
        quantity_delta=payload.quantity,
        current_user=current_user,
        note=payload.note,
    )


def register_exit(
    db: Session,
    payload: MovementCreate,
    current_user: User,
) -> dict[str, object]:
    return register_movement(
        db,
        product_id=payload.product_id,
        movement_type=MovementType.EXIT,
        quantity_delta=-payload.quantity,
        current_user=current_user,
        note=payload.note,
    )


def register_adjustment(
    db: Session,
    payload: AdjustmentCreate,
    current_user: User,
) -> dict[str, object]:
    if payload.quantity_delta == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Adjustment delta cannot be zero.",
        )

    return register_movement(
        db,
        product_id=payload.product_id,
        movement_type=MovementType.ADJUSTMENT,
        quantity_delta=payload.quantity_delta,
        current_user=current_user,
        reason=payload.reason.strip(),
        note=payload.note,
    )


def register_movement(
    db: Session,
    *,
    product_id: int,
    movement_type: MovementType,
    quantity_delta: Decimal,
    current_user: User,
    reason: str | None = None,
    note: str | None = None,
) -> dict[str, object]:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    if not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Inactive product cannot receive movements.",
        )

    balance = db.scalar(
        select(InventoryBalance)
        .where(InventoryBalance.product_id == product_id)
        .with_for_update(),
    )
    if balance is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product balance not found.",
        )

    balance_before = balance.quantity
    balance_after = balance_before + quantity_delta
    if balance_after < 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Insufficient balance.",
        )

    movement = StockMovement(
        product_id=product_id,
        created_by_id=current_user.id,
        type=movement_type,
        quantity_delta=quantity_delta,
        balance_before=balance_before,
        balance_after=balance_after,
        reason=reason,
        note=note.strip() if note else None,
    )
    balance.quantity = balance_after
    db.add(movement)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    db.refresh(movement)
    db.refresh(balance)
    return movement_to_response(movement, product, current_user)


def list_movements(
    db: Session,
    *,
    product_id: int | None = None,
    movement_type: MovementType | None = None,
) -> list[dict[str, object]]:
    statement: Select[tuple[StockMovement, Product, User]] = (
        select(StockMovement, Product, User)
        .join(Product, Product.id == StockMovement.product_id)
        .join(User, User.id == StockMovement.created_by_id)
    )
    if product_id is not None:
        statement = statement.where(StockMovement.product_id == product_id)
    if movement_type is not None:
        statement = statement.where(StockMovement.type == movement_type)

    rows = db.execute(statement.order_by(StockMovement.created_at.desc())).all()
    return [
        movement_to_response(movement, product, user)
        for movement, product, user in rows
    ]


def movement_to_response(
    movement: StockMovement,
    product: Product,
    user: User,
) -> dict[str, object]:
    return {
        "id": movement.id,
        "product_id": movement.product_id,
        "product_name": product.name,
        "product_sku": product.sku,
        "created_by_id": movement.created_by_id,
        "created_by_name": user.name,
        "type": movement.type,
        "quantity_delta": movement.quantity_delta,
        "balance_before": movement.balance_before,
        "balance_after": movement.balance_after,
        "reason": movement.reason,
        "note": movement.note,
        "created_at": movement.created_at,
    }
