from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_db
from app.db.base import Base
from app.main import app
from app.models.user import UserRole
from app.schemas.inventory import CategoryCreate, ProductCreate
from app.schemas.user import UserCreate
from app.services.inventory import create_category, create_product
from app.services.users import create_user

TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"


@pytest.fixture
def db_session() -> Generator[Session]:
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as session:
        yield session


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient]:
    def override_get_db() -> Generator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def create_test_user(db: Session, *, email: str, role: UserRole):
    return create_user(
        db,
        UserCreate(
            name="Test User",
            email=email,
            password="strong-password",
            role=role,
            is_active=True,
        ),
    )


def login(client: TestClient, email: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "strong-password"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def create_catalog_product(db: Session):
    category = create_category(
        db,
        CategoryCreate(name="Informatica", description=None),
    )
    return create_product(
        db,
        ProductCreate(
            name="Mouse",
            sku="MOU-001",
            category_id=category.id,
            unit="UN",
            minimum_stock="1.000",
        ),
    )


def test_supplier_tax_id_validation_and_uniqueness(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="manager@example.com", role=UserRole.MANAGER)
    token = login(client, "manager@example.com")

    created = client.post(
        "/api/v1/suppliers",
        headers=auth_header(token),
        json={
            "name": "Fornecedor Um",
            "tax_id": "12.345.678/0001-95",
            "email": "contato@fornecedor.com",
            "phone": "(11) 99999-0000",
        },
    )
    duplicate = client.post(
        "/api/v1/suppliers",
        headers=auth_header(token),
        json={"name": "Duplicado", "tax_id": "12345678000195"},
    )
    invalid = client.post(
        "/api/v1/suppliers",
        headers=auth_header(token),
        json={"name": "Invalido", "tax_id": "11.111.111/1111-11"},
    )

    assert created.status_code == 201
    assert created.json()["tax_id"] == "12.345.678/0001-95"
    assert duplicate.status_code == 409
    assert invalid.status_code == 422


def test_operator_can_read_but_not_manage_suppliers(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="manager@example.com", role=UserRole.MANAGER)
    create_test_user(db_session, email="operator@example.com", role=UserRole.OPERATOR)
    manager_token = login(client, "manager@example.com")
    operator_token = login(client, "operator@example.com")

    client.post(
        "/api/v1/suppliers",
        headers=auth_header(manager_token),
        json={"name": "Fornecedor Leitura"},
    )
    read = client.get("/api/v1/suppliers", headers=auth_header(operator_token))
    create = client.post(
        "/api/v1/suppliers",
        headers=auth_header(operator_token),
        json={"name": "Operador"},
    )

    assert read.status_code == 200
    assert read.json()[0]["name"] == "Fornecedor Leitura"
    assert create.status_code == 403


def test_product_supplier_links_require_active_records_and_are_unique(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="admin@example.com", role=UserRole.ADMIN)
    token = login(client, "admin@example.com")
    product = create_catalog_product(db_session)
    supplier = client.post(
        "/api/v1/suppliers",
        headers=auth_header(token),
        json={"name": "Fornecedor Ativo"},
    ).json()

    created = client.post(
        f"/api/v1/products/{product.id}/suppliers",
        headers=auth_header(token),
        json={"supplier_id": supplier["id"]},
    )
    duplicate = client.post(
        f"/api/v1/products/{product.id}/suppliers",
        headers=auth_header(token),
        json={"supplier_id": supplier["id"]},
    )
    listed = client.get(
        f"/api/v1/products/{product.id}/suppliers",
        headers=auth_header(token),
    )
    removed = client.delete(
        f"/api/v1/products/{product.id}/suppliers/{supplier['id']}",
        headers=auth_header(token),
    )
    listed_after_remove = client.get(
        f"/api/v1/products/{product.id}/suppliers",
        headers=auth_header(token),
    )

    assert created.status_code == 201
    assert duplicate.status_code == 409
    assert listed.status_code == 200
    assert listed.json()[0]["supplier_name"] == "Fornecedor Ativo"
    assert removed.status_code == 204
    assert listed_after_remove.json() == []


def test_inactive_product_or_supplier_rejects_new_link(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="manager@example.com", role=UserRole.MANAGER)
    token = login(client, "manager@example.com")
    product = create_catalog_product(db_session)
    supplier = client.post(
        "/api/v1/suppliers",
        headers=auth_header(token),
        json={"name": "Fornecedor Inativo"},
    ).json()
    client.patch(
        f"/api/v1/suppliers/{supplier['id']}",
        headers=auth_header(token),
        json={"is_active": False},
    )

    inactive_supplier = client.post(
        f"/api/v1/products/{product.id}/suppliers",
        headers=auth_header(token),
        json={"supplier_id": supplier["id"]},
    )
    product.is_active = False
    db_session.commit()
    active_supplier = client.post(
        "/api/v1/suppliers",
        headers=auth_header(token),
        json={"name": "Fornecedor Dois"},
    ).json()
    inactive_product = client.post(
        f"/api/v1/products/{product.id}/suppliers",
        headers=auth_header(token),
        json={"supplier_id": active_supplier["id"]},
    )

    assert inactive_supplier.status_code == 409
    assert inactive_product.status_code == 409
