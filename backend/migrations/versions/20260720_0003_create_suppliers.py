"""create suppliers

Revision ID: 20260720_0003
Revises: 20260720_0002
Create Date: 2026-07-20

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260720_0003"
down_revision: str | None = "20260720_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("tax_id", sa.String(length=20), nullable=True),
        sa.Column("normalized_tax_id", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=254), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.Column("normalized_phone", sa.String(length=30), nullable=True),
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
        op.f("ix_suppliers_normalized_tax_id"),
        "suppliers",
        ["normalized_tax_id"],
        unique=True,
    )

    op.create_table(
        "product_suppliers",
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"]),
        sa.PrimaryKeyConstraint("product_id", "supplier_id"),
    )


def downgrade() -> None:
    op.drop_table("product_suppliers")
    op.drop_index(op.f("ix_suppliers_normalized_tax_id"), table_name="suppliers")
    op.drop_table("suppliers")
