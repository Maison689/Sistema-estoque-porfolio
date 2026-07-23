from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.inventory import InventoryBalance, MovementType, Product, StockMovement
from app.models.user import User
from app.services.inventory import product_to_response
from app.services.movements import movement_to_response


def get_dashboard(db: Session) -> dict[str, object]:
    active_products = count_products(db, is_active=True)
    inactive_products = count_products(db, is_active=False)
    low_stock_rows = get_low_stock_rows(db)
    total_movements = db.scalar(select(func.count()).select_from(StockMovement)) or 0

    return {
        "low_stock_products": [
            product_to_response(product, product.category, balance)
            for product, balance in low_stock_rows
        ],
        "metrics": {
            "active_products": active_products,
            "inactive_products": inactive_products,
            "low_stock_products": len(low_stock_rows),
            "total_movements": total_movements,
        },
        "movement_summary": get_movement_summary(db),
        "recent_movements": get_recent_movements(db),
    }


def count_products(db: Session, *, is_active: bool) -> int:
    return (
        db.scalar(
            select(func.count()).select_from(Product).where(
                Product.is_active.is_(is_active),
            ),
        )
        or 0
    )


def get_low_stock_rows(
    db: Session,
    *,
    limit: int = 10,
) -> list[tuple[Product, InventoryBalance]]:
    return list(
        db.execute(
            select(Product, InventoryBalance)
            .join(InventoryBalance, InventoryBalance.product_id == Product.id)
            .where(
                Product.is_active.is_(True),
                InventoryBalance.quantity < Product.minimum_stock,
            )
            .order_by((Product.minimum_stock - InventoryBalance.quantity).desc())
            .limit(limit),
        ).all(),
    )


def get_movement_summary(db: Session) -> list[dict[str, object]]:
    rows = db.execute(
        select(
            StockMovement.type,
            func.count(StockMovement.id),
            func.coalesce(func.sum(StockMovement.quantity_delta), Decimal("0.000")),
        )
        .group_by(StockMovement.type)
        .order_by(StockMovement.type),
    ).all()
    summary_by_type = {
        movement_type: {
            "count": count,
            "quantity_delta_total": quantity_delta_total,
            "type": movement_type,
        }
        for movement_type, count, quantity_delta_total in rows
    }
    return [
        summary_by_type.get(
            movement_type,
            {
                "count": 0,
                "quantity_delta_total": Decimal("0.000"),
                "type": movement_type,
            },
        )
        for movement_type in MovementType
    ]


def get_recent_movements(db: Session, *, limit: int = 5) -> list[dict[str, object]]:
    rows = db.execute(
        select(StockMovement, Product, User)
        .join(Product, Product.id == StockMovement.product_id)
        .join(User, User.id == StockMovement.created_by_id)
        .order_by(StockMovement.created_at.desc())
        .limit(limit),
    ).all()
    return [
        movement_to_response(movement, product, user)
        for movement, product, user in rows
    ]
