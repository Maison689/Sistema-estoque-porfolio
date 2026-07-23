import os
from decimal import Decimal

from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models.inventory import Product, ProductUnit, StockMovement
from app.models.supplier import Supplier
from app.schemas.inventory import CategoryCreate, ProductCreate
from app.schemas.movement import AdjustmentCreate, MovementCreate
from app.schemas.supplier import SupplierCreate
from app.services.inventory import (
    create_category,
    create_product,
    get_product_by_id,
    list_categories,
    list_products,
)
from app.services.movements import register_adjustment, register_entry, register_exit
from app.services.suppliers import (
    create_product_supplier,
    create_supplier,
    get_supplier_by_id,
    list_product_suppliers,
    list_suppliers,
)
from app.services.users import get_user_by_email


def main() -> None:
    admin_email = os.environ["DEMO_ADMIN_EMAIL"]

    with SessionLocal() as db:
        user = get_user_by_email(db, admin_email)
        if user is None:
            raise RuntimeError("DEMO_ADMIN_EMAIL must reference an existing user.")

        categories = list_categories(db, search="Demo")
        category = categories[0] if categories else create_category(
            db,
            CategoryCreate(
                name="Demo",
                description="Categoria de demonstracao local",
            ),
        )

        keyboard = get_or_create_product(
            db,
            name="Teclado demo",
            sku="DEMO-TEC",
            category_id=category.id,
            minimum_stock=Decimal("5.000"),
        )
        mouse = get_or_create_product(
            db,
            name="Mouse demo",
            sku="DEMO-MOU",
            category_id=category.id,
            minimum_stock=Decimal("10.000"),
        )

        suppliers = list_suppliers(db, search="Fornecedor Demo")
        supplier = (
            get_supplier_by_id(db, int(suppliers[0]["id"]))
            if suppliers
            else create_supplier(
                db,
                SupplierCreate(
                    name="Fornecedor Demo",
                    email="demo@example.com",
                    phone="(11) 90000-0000",
                ),
            )
        )
        ensure_link(db, keyboard, supplier)
        ensure_link(db, mouse, supplier)

        if not has_movements(db, keyboard.id):
            register_entry(
                db,
                MovementCreate(
                    product_id=keyboard.id,
                    quantity=Decimal("7.000"),
                    note="Carga inicial de demonstracao",
                ),
                user,
            )
            register_exit(
                db,
                MovementCreate(
                    product_id=keyboard.id,
                    quantity=Decimal("2.000"),
                    note="Saida de demonstracao",
                ),
                user,
            )
        if not has_movements(db, mouse.id):
            register_entry(
                db,
                MovementCreate(
                    product_id=mouse.id,
                    quantity=Decimal("4.000"),
                    note="Carga inicial de demonstracao",
                ),
                user,
            )
            register_adjustment(
                db,
                AdjustmentCreate(
                    product_id=mouse.id,
                    quantity_delta=Decimal("1.000"),
                    reason="Conferencia de demonstracao",
                ),
                user,
            )

    print("Demo data created.")


def get_or_create_product(
    db,
    *,
    category_id: int,
    minimum_stock: Decimal,
    name: str,
    sku: str,
) -> Product:
    products = list_products(db, search=sku)
    if products:
        product = get_product_by_id(db, int(products[0]["id"]))
        if product is None:
            raise RuntimeError("Demo product lookup failed.")
        return product

    return create_product(
        db,
        ProductCreate(
            name=name,
            sku=sku,
            category_id=category_id,
            unit=ProductUnit.UN,
            minimum_stock=minimum_stock,
        ),
    )


def ensure_link(db, product: Product, supplier: Supplier) -> None:
    existing_links = list_product_suppliers(db, product.id)
    if any(link["supplier_id"] == supplier.id for link in existing_links):
        return
    create_product_supplier(db, product.id, supplier.id)


def has_movements(db, product_id: int) -> bool:
    count = db.scalar(
        select(func.count()).select_from(StockMovement).where(
            StockMovement.product_id == product_id,
        ),
    )
    return bool(count)


if __name__ == "__main__":
    main()
