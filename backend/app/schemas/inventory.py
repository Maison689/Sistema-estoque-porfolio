from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.inventory import ProductUnit


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    is_active: bool = True


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    is_active: bool


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    sku: str = Field(min_length=1, max_length=64)
    category_id: int
    unit: ProductUnit
    minimum_stock: Decimal = Field(ge=0, max_digits=12, decimal_places=3)
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    sku: str | None = Field(default=None, min_length=1, max_length=64)
    category_id: int | None = None
    unit: ProductUnit | None = None
    minimum_stock: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=12,
        decimal_places=3,
    )
    is_active: bool | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    category_id: int
    category_name: str
    unit: ProductUnit
    minimum_stock: Decimal
    quantity: Decimal
    is_active: bool
    is_below_minimum: bool
