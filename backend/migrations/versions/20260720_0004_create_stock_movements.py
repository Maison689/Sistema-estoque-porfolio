"""create stock movements

Revision ID: 20260720_0004
Revises: 20260720_0003
Create Date: 2026-07-20

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260720_0004"
down_revision: str | None = "20260720_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

movement_type = postgresql.ENUM(
    "ENTRY",
    "EXIT",
    "ADJUSTMENT",
    name="movementtype",
)


def upgrade() -> None:
    movement_type.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "stock_movements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            postgresql.ENUM(
                "ENTRY",
                "EXIT",
                "ADJUSTMENT",
                name="movementtype",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("quantity_delta", sa.Numeric(12, 3), nullable=False),
        sa.Column("balance_before", sa.Numeric(12, 3), nullable=False),
        sa.Column("balance_after", sa.Numeric(12, 3), nullable=False),
        sa.Column("reason", sa.String(length=500), nullable=True),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "quantity_delta <> 0",
            name="ck_stock_movements_delta_non_zero",
        ),
        sa.CheckConstraint(
            "balance_before >= 0",
            name="ck_stock_movements_balance_before_non_negative",
        ),
        sa.CheckConstraint(
            "balance_after >= 0",
            name="ck_stock_movements_balance_after_non_negative",
        ),
        sa.CheckConstraint(
            "balance_after = balance_before + quantity_delta",
            name="ck_stock_movements_balance_math",
        ),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_stock_movements_product_created_at",
        "stock_movements",
        ["product_id", "created_at"],
    )
    op.create_index(
        "ix_stock_movements_type_created_at",
        "stock_movements",
        ["type", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_stock_movements_type_created_at", table_name="stock_movements")
    op.drop_index("ix_stock_movements_product_created_at", table_name="stock_movements")
    op.drop_table("stock_movements")
    movement_type.drop(op.get_bind(), checkfirst=True)
