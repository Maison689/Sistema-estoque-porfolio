from fastapi import HTTPException, status
from sqlalchemy import Select, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.inventory import Product
from app.models.supplier import ProductSupplier, Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate


def only_digits(value: str) -> str:
    return "".join(character for character in value if character.isdigit())


def normalize_tax_id(value: str | None) -> str | None:
    if not value:
        return None
    return only_digits(value)


def normalize_phone(value: str | None) -> str | None:
    if not value:
        return None
    return only_digits(value) or value.strip()


def validate_tax_id(value: str | None) -> str | None:
    normalized = normalize_tax_id(value)
    if normalized is None:
        return None
    if len(normalized) == 11 and is_valid_cpf(normalized):
        return normalized
    if len(normalized) == 14 and is_valid_cnpj(normalized):
        return normalized
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail="Tax ID must be a valid CPF or CNPJ.",
    )


def is_valid_cpf(value: str) -> bool:
    if len(value) != 11 or len(set(value)) == 1:
        return False
    first = sum(int(value[index]) * (10 - index) for index in range(9))
    first_digit = (first * 10 % 11) % 10
    second = sum(int(value[index]) * (11 - index) for index in range(10))
    second_digit = (second * 10 % 11) % 10
    return value[-2:] == f"{first_digit}{second_digit}"


def is_valid_cnpj(value: str) -> bool:
    if len(value) != 14 or len(set(value)) == 1:
        return False
    weights_first = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weights_second = [6, *weights_first]
    first_sum = sum(
        int(digit) * weight
        for digit, weight in zip(value[:12], weights_first, strict=True)
    )
    first_digit = 0 if first_sum % 11 < 2 else 11 - (first_sum % 11)
    second_sum = sum(
        int(digit) * weight
        for digit, weight in zip(
            f"{value[:12]}{first_digit}",
            weights_second,
            strict=True,
        )
    )
    second_digit = 0 if second_sum % 11 < 2 else 11 - (second_sum % 11)
    return value[-2:] == f"{first_digit}{second_digit}"


def list_suppliers(
    db: Session,
    *,
    search: str | None = None,
    is_active: bool | None = None,
) -> list[dict[str, object]]:
    product_count = func.count(ProductSupplier.product_id).label("products_count")
    statement: Select[tuple[Supplier, int]] = (
        select(Supplier, product_count)
        .outerjoin(ProductSupplier, ProductSupplier.supplier_id == Supplier.id)
        .group_by(Supplier.id)
    )
    if search:
        term = f"%{search.strip()}%"
        digits = normalize_tax_id(search)
        statement = statement.where(
            Supplier.name.ilike(term)
            | Supplier.email.ilike(term)
            | Supplier.normalized_tax_id.contains(digits or ""),
        )
    if is_active is not None:
        statement = statement.where(Supplier.is_active == is_active)

    rows = db.execute(statement.order_by(Supplier.name)).all()
    return [
        supplier_to_response(supplier, products_count)
        for supplier, products_count in rows
    ]


def get_supplier_by_id(db: Session, supplier_id: int) -> Supplier | None:
    return db.get(Supplier, supplier_id)


def create_supplier(db: Session, payload: SupplierCreate) -> Supplier:
    supplier = Supplier(
        name=payload.name.strip(),
        tax_id=payload.tax_id.strip() if payload.tax_id else None,
        normalized_tax_id=validate_tax_id(payload.tax_id),
        email=str(payload.email) if payload.email else None,
        phone=payload.phone.strip() if payload.phone else None,
        normalized_phone=normalize_phone(payload.phone),
        is_active=payload.is_active,
    )
    db.add(supplier)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(supplier)
    return supplier


def update_supplier(
    db: Session,
    supplier: Supplier,
    payload: SupplierUpdate,
) -> Supplier:
    if payload.name is not None:
        supplier.name = payload.name.strip()
    if payload.tax_id is not None:
        supplier.tax_id = payload.tax_id.strip() if payload.tax_id else None
        supplier.normalized_tax_id = validate_tax_id(payload.tax_id)
    if payload.email is not None:
        supplier.email = str(payload.email)
    if payload.phone is not None:
        supplier.phone = payload.phone.strip() if payload.phone else None
        supplier.normalized_phone = normalize_phone(payload.phone)
    if payload.is_active is not None:
        supplier.is_active = payload.is_active

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(supplier)
    return supplier


def list_product_suppliers(
    db: Session,
    product_id: int,
) -> list[dict[str, object]]:
    require_existing_product(db, product_id)
    statement = (
        select(ProductSupplier, Supplier)
        .join(Supplier, Supplier.id == ProductSupplier.supplier_id)
        .where(ProductSupplier.product_id == product_id)
        .order_by(Supplier.name)
    )
    return [
        product_supplier_to_response(link, supplier)
        for link, supplier in db.execute(statement).all()
    ]


def create_product_supplier(
    db: Session,
    product_id: int,
    supplier_id: int,
) -> ProductSupplier:
    product = require_existing_product(db, product_id)
    supplier = get_supplier_by_id(db, supplier_id)
    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found.",
        )
    if not product.is_active or not supplier.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product and supplier must be active.",
        )

    link = ProductSupplier(product_id=product_id, supplier_id=supplier_id)
    db.add(link)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(link)
    return link


def delete_product_supplier(db: Session, product_id: int, supplier_id: int) -> None:
    link = db.get(
        ProductSupplier,
        {"product_id": product_id, "supplier_id": supplier_id},
    )
    if link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found.",
        )
    db.delete(link)
    db.commit()


def require_existing_product(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    return product


def supplier_to_response(
    supplier: Supplier,
    products_count: int = 0,
) -> dict[str, object]:
    return {
        "id": supplier.id,
        "name": supplier.name,
        "tax_id": supplier.tax_id,
        "email": supplier.email,
        "phone": supplier.phone,
        "is_active": supplier.is_active,
        "products_count": products_count,
    }


def product_supplier_to_response(
    link: ProductSupplier,
    supplier: Supplier,
) -> dict[str, object]:
    return {
        "product_id": link.product_id,
        "supplier_id": link.supplier_id,
        "supplier_name": supplier.name,
        "supplier_tax_id": supplier.tax_id,
        "supplier_email": supplier.email,
        "supplier_phone": supplier.phone,
    }
