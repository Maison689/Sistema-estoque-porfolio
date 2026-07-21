from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.inventory import MovementType


class MovementCreate(BaseModel):
    product_id: int
    quantity: Decimal = Field(gt=0, max_digits=12, decimal_places=3)
    note: str | None = Field(default=None, max_length=500)


class AdjustmentCreate(BaseModel):
    product_id: int
    quantity_delta: Decimal = Field(max_digits=12, decimal_places=3)
    reason: str = Field(min_length=1, max_length=500)
    note: str | None = Field(default=None, max_length=500)


class MovementResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_sku: str
    created_by_id: int
    created_by_name: str
    type: MovementType
    quantity_delta: Decimal
    balance_before: Decimal
    balance_after: Decimal
    reason: str | None
    note: str | None
    created_at: datetime
