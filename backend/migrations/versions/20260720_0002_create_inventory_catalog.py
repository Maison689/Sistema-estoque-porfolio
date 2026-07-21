"""create inventory catalog

Revision ID: 20260720_0002
Revises: 20260720_0001
Create Date: 2026-07-20

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260720_0002"
down_revision: str | None = "20260720_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

product_unit = postgresql.ENUM(
    "UN",
    "CX",
    "KG",
    "G",
    "L",
    "ML",
    "M",
    "CM",
    name="productunit",
)


def upgrade() -> None:
    bind = op.get_bind()
    product_unit.create(bind, checkfirst=True)

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("normalized_name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_categories_normalized_name"),
        "categories",
        ["normalized_name"],
        unique=True,
    )

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("sku", sa.String(length=64), nullable=False),
        sa.Column("normalized_sku", sa.String(length=64), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column(
            "unit",
            postgresql.ENUM(
                "UN",
                "CX",
                "KG",
                "G",
                "L",
                "ML",
                "M",
                "CM",
                name="productunit",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("minimum_stock", sa.Numeric(12, 3), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "minimum_stock >= 0",
            name="ck_products_minimum_stock_non_negative",
        ),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_products_normalized_sku"),
        "products",
        ["normalized_sku"],
        unique=True,
    )

    op.create_table(
        "inventory_balances",
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "quantity >= 0",
            name="ck_inventory_balances_quantity_non_negative",
        ),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("product_id"),
    )


def downgrade() -> None:
    op.drop_table("inventory_balances")
    op.drop_index(op.f("ix_products_normalized_sku"), table_name="products")
    op.drop_table("products")
    op.drop_index(op.f("ix_categories_normalized_name"), table_name="categories")
    op.drop_table("categories")
    product_unit.drop(op.get_bind(), checkfirst=True)
