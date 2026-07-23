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
    category = create_category(db, CategoryCreate(name="Informatica"))
    return create_product(
        db,
        ProductCreate(
            name="Mouse",
            sku="MOU-001",
            category_id=category.id,
            unit="UN",
            minimum_stock="5.000",
        ),
    )


def test_dashboard_uses_official_stock_and_movement_data(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="admin@example.com", role=UserRole.ADMIN)
    token = login(client, "admin@example.com")
    product = create_catalog_product(db_session)

    client.post(
        "/api/v1/movements/entries",
        headers=auth_header(token),
        json={"product_id": product.id, "quantity": "2.000"},
    )

    response = client.get("/api/v1/dashboard", headers=auth_header(token))

    assert response.status_code == 200
    body = response.json()
    assert body["metrics"]["active_products"] == 1
    assert body["metrics"]["low_stock_products"] == 1
    assert body["metrics"]["total_movements"] == 1
    assert body["low_stock_products"][0]["name"] == "Mouse"
    assert body["recent_movements"][0]["balance_after"] == "2.000"


def test_operator_cannot_access_dashboard(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="operator@example.com", role=UserRole.OPERATOR)
    token = login(client, "operator@example.com")

    response = client.get("/api/v1/dashboard", headers=auth_header(token))

    assert response.status_code == 403
