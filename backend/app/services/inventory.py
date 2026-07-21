from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import Select, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.inventory import Category, InventoryBalance, Product
from app.schemas.inventory import (
    CategoryCreate,
    CategoryUpdate,
    ProductCreate,
    ProductUpdate,
)


def normalize_lookup(value: str) -> str:
    return " ".join(value.strip().lower().split())


def normalize_sku(value: str) -> str:
    return value.strip().upper()


def list_categories(
    db: Session,
    *,
    search: str | None = None,
    is_active: bool | None = None,
) -> list[Category]:
    statement = select(Category)
    if search:
        statement = statement.where(
            Category.normalized_name.contains(normalize_lookup(search)),
        )
    if is_active is not None:
        statement = statement.where(Category.is_active == is_active)

    return list(db.scalars(statement.order_by(Category.name)))


def get_category_by_id(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)


def create_category(db: Session, payload: CategoryCreate) -> Category:
    category = Category(
        name=payload.name.strip(),
        normalized_name=normalize_lookup(payload.name),
        description=payload.description.strip() if payload.description else None,
        is_active=payload.is_active,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(
    db: Session,
    category: Category,
    payload: CategoryUpdate,
) -> Category:
    if payload.name is not None:
        category.name = payload.name.strip()
        category.normalized_name = normalize_lookup(payload.name)
    if payload.description is not None:
        category.description = payload.description.strip() or None
    if payload.is_active is not None:
        if not payload.is_active and category_has_active_products(db, category.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category with active products cannot be deactivated.",
            )
        category.is_active = payload.is_active

    db.commit()
    db.refresh(category)
    return category


def category_has_active_products(db: Session, category_id: int) -> bool:
    count = db.scalar(
        select(func.count()).select_from(Product).where(
            Product.category_id == category_id,
            Product.is_active.is_(True),
        ),
    )
    return bool(count)


def list_products(
    db: Session,
    *,
    search: str | None = None,
    category_id: int | None = None,
    is_active: bool | None = None,
    stock_status: str | None = None,
) -> list[dict[str, object]]:
    statement: Select[tuple[Product, Category, InventoryBalance]] = (
        select(Product, Category, InventoryBalance)
        .join(Category, Product.category_id == Category.id)
        .join(InventoryBalance, InventoryBalance.product_id == Product.id)
    )
    if search:
        normalized_search = normalize_lookup(search)
        sku_search = normalize_sku(search)
        statement = statement.where(
            Product.name.ilike(f"%{search.strip()}%")
            | Product.normalized_sku.contains(sku_search)
            | Product.sku.ilike(f"%{search.strip()}%")
            | Category.normalized_name.contains(normalized_search),
        )
    if category_id is not None:
        statement = statement.where(Product.category_id == category_id)
    if is_active is not None:
        statement = statement.where(Product.is_active == is_active)
    if stock_status == "below_minimum":
        statement = statement.where(InventoryBalance.quantity < Product.minimum_stock)
    elif stock_status == "within_minimum":
        statement = statement.where(InventoryBalance.quantity >= Product.minimum_stock)

    rows = db.execute(statement.order_by(Product.name)).all()
    return [
        product_to_response(product, category, balance)
        for product, category, balance in rows
    ]


def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def create_product(db: Session, payload: ProductCreate) -> Product:
    category = require_active_category(db, payload.category_id)
    product = Product(
        name=payload.name.strip(),
        sku=payload.sku.strip(),
        normalized_sku=normalize_sku(payload.sku),
        category_id=category.id,
        unit=payload.unit,
        minimum_stock=payload.minimum_stock,
        is_active=payload.is_active,
    )
    product.balance = InventoryBalance(quantity=Decimal("0.000"))
    db.add(product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, payload: ProductUpdate) -> Product:
    if payload.name is not None:
        product.name = payload.name.strip()
    if payload.sku is not None:
        product.sku = payload.sku.strip()
        product.normalized_sku = normalize_sku(payload.sku)
    if payload.category_id is not None:
        product.category_id = require_active_category(db, payload.category_id).id
    if payload.unit is not None:
        product.unit = payload.unit
    if payload.minimum_stock is not None:
        product.minimum_stock = payload.minimum_stock
    if payload.is_active is not None:
        product.is_active = payload.is_active

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(product)
    return product


def require_active_category(db: Session, category_id: int) -> Category:
    category = get_category_by_id(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )
    if not category.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product requires an active category.",
        )

    return category


def product_to_response(
    product: Product,
    category: Category | None = None,
    balance: InventoryBalance | None = None,
) -> dict[str, object]:
    product_category = category or product.category
    product_balance = balance or product.balance
    quantity = product_balance.quantity
    return {
        "id": product.id,
        "name": product.name,
        "sku": product.sku,
        "category_id": product.category_id,
        "category_name": product_category.name,
        "unit": product.unit,
        "minimum_stock": product.minimum_stock,
        "quantity": quantity,
        "is_active": product.is_active,
        "is_below_minimum": quantity < product.minimum_stock,
    }
