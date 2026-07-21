from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class SupplierCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    tax_id: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    is_active: bool = True

    @field_validator("tax_id", "phone")
    @classmethod
    def blank_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class SupplierUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    tax_id: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    is_active: bool | None = None

    @field_validator("tax_id", "phone")
    @classmethod
    def blank_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class SupplierResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    tax_id: str | None
    email: EmailStr | None
    phone: str | None
    is_active: bool
    products_count: int = 0


class ProductSupplierCreate(BaseModel):
    supplier_id: int


class ProductSupplierResponse(BaseModel):
    product_id: int
    supplier_id: int
    supplier_name: str
    supplier_tax_id: str | None
    supplier_email: EmailStr | None
    supplier_phone: str | None
