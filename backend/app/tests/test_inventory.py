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
from app.schemas.user import UserCreate
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


def create_category(client: TestClient, token: str, name: str = "Informatica"):
    response = client.post(
        "/api/v1/categories",
        headers=auth_header(token),
        json={"name": name, "description": "Itens de tecnologia"},
    )
    assert response.status_code == 201
    return response.json()


def test_categories_are_unique_and_operator_can_only_read(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="manager@example.com", role=UserRole.MANAGER)
    create_test_user(db_session, email="operator@example.com", role=UserRole.OPERATOR)
    manager_token = login(client, "manager@example.com")
    operator_token = login(client, "operator@example.com")

    created = create_category(client, manager_token)
    duplicate = client.post(
        "/api/v1/categories",
        headers=auth_header(manager_token),
        json={"name": "informatica"},
    )
    operator_create = client.post(
        "/api/v1/categories",
        headers=auth_header(operator_token),
        json={"name": "Operador"},
    )
    operator_read = client.get(
        "/api/v1/categories",
        headers=auth_header(operator_token),
    )

    assert created["name"] == "Informatica"
    assert duplicate.status_code == 409
    assert operator_create.status_code == 403
    assert operator_read.status_code == 200
    assert operator_read.json()[0]["name"] == "Informatica"


def test_product_creation_requires_active_category_and_starts_with_zero_balance(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="admin@example.com", role=UserRole.ADMIN)
    admin_token = login(client, "admin@example.com")
    category = create_category(client, admin_token)

    product = client.post(
        "/api/v1/products",
        headers=auth_header(admin_token),
        json={
            "name": "Mouse sem fio",
            "sku": "ms-001",
            "category_id": category["id"],
            "unit": "UN",
            "minimum_stock": "5.000",
        },
    )
    duplicate = client.post(
        "/api/v1/products",
        headers=auth_header(admin_token),
        json={
            "name": "Mouse duplicado",
            "sku": "MS-001",
            "category_id": category["id"],
            "unit": "UN",
            "minimum_stock": "1.000",
        },
    )
    inactivate = client.patch(
        f"/api/v1/categories/{category['id']}",
        headers=auth_header(admin_token),
        json={"is_active": False},
    )

    assert product.status_code == 201
    body = product.json()
    assert body["quantity"] == "0.000"
    assert body["is_below_minimum"] is True
    assert "balance" not in body
    assert duplicate.status_code == 409
    assert inactivate.status_code == 409


def test_product_permissions_and_validations(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="manager@example.com", role=UserRole.MANAGER)
    create_test_user(db_session, email="operator@example.com", role=UserRole.OPERATOR)
    manager_token = login(client, "manager@example.com")
    operator_token = login(client, "operator@example.com")
    category = create_category(client, manager_token)
    client.patch(
        f"/api/v1/categories/{category['id']}",
        headers=auth_header(manager_token),
        json={"is_active": False},
    )

    invalid_category = client.post(
        "/api/v1/products",
        headers=auth_header(manager_token),
        json={
            "name": "Mesa",
            "sku": "MESA-001",
            "category_id": category["id"],
            "unit": "UN",
            "minimum_stock": "0.000",
        },
    )
    negative_minimum = client.post(
        "/api/v1/products",
        headers=auth_header(manager_token),
        json={
            "name": "Cadeira",
            "sku": "CAD-001",
            "category_id": category["id"],
            "unit": "UN",
            "minimum_stock": "-1.000",
        },
    )
    operator_create = client.post(
        "/api/v1/products",
        headers=auth_header(operator_token),
        json={
            "name": "Monitor",
            "sku": "MON-001",
            "category_id": category["id"],
            "unit": "UN",
            "minimum_stock": "1.000",
        },
    )
    operator_read = client.get("/api/v1/products", headers=auth_header(operator_token))

    assert invalid_category.status_code == 409
    assert negative_minimum.status_code == 422
    assert operator_create.status_code == 403
    assert operator_read.status_code == 200
