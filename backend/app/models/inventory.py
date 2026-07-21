from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    func,
)
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ProductUnit(StrEnum):
    UN = "UN"
    CX = "CX"
    KG = "KG"
    G = "G"
    L = "L"
    ML = "ML"
    M = "M"
    CM = "CM"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    normalized_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint(
            "minimum_stock >= 0",
            name="ck_products_minimum_stock_non_negative",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    sku: Mapped[str] = mapped_column(String(64), nullable=False)
    normalized_sku: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )
    unit: Mapped[ProductUnit] = mapped_column(SqlEnum(ProductUnit), nullable=False)
    minimum_stock: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    category: Mapped[Category] = relationship(back_populates="products")
    balance: Mapped["InventoryBalance"] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        uselist=False,
    )


class InventoryBalance(Base):
    __tablename__ = "inventory_balances"
    __table_args__ = (
        CheckConstraint(
            "quantity >= 0",
            name="ck_inventory_balances_quantity_non_negative",
        ),
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        primary_key=True,
    )
    quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        nullable=False,
        default=Decimal("0.000"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    product: Mapped[Product] = relationship(back_populates="balance")
