from decimal import Decimal

from pydantic import BaseModel

from app.models.inventory import MovementType
from app.schemas.inventory import ProductResponse
from app.schemas.movement import MovementResponse


class DashboardMetrics(BaseModel):
    active_products: int
    inactive_products: int
    low_stock_products: int
    total_movements: int


class MovementTypeSummary(BaseModel):
    count: int
    quantity_delta_total: Decimal
    type: MovementType


class DashboardResponse(BaseModel):
    low_stock_products: list[ProductResponse]
    metrics: DashboardMetrics
    movement_summary: list[MovementTypeSummary]
    recent_movements: list[MovementResponse]
