from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    tax_id: Mapped[str | None] = mapped_column(String(20), nullable=True)
    normalized_tax_id: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        unique=True,
        index=True,
    )
    email: Mapped[str | None] = mapped_column(String(254), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    normalized_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
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
    product_links: Mapped[list["ProductSupplier"]] = relationship(
        back_populates="supplier",
        cascade="all, delete-orphan",
    )


class ProductSupplier(Base):
    __tablename__ = "product_suppliers"

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        primary_key=True,
    )
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id"),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    supplier: Mapped[Supplier] = relationship(back_populates="product_links")
