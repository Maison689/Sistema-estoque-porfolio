from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_db
from app.db.base import Base
from app.main import app
from app.models.inventory import InventoryBalance
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
            minimum_stock="1.000",
        ),
    )


def get_balance(db: Session, product_id: int):
    return db.get(InventoryBalance, product_id).quantity


def test_entry_exit_and_history_update_balance_atomically(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="operator@example.com", role=UserRole.OPERATOR)
    token = login(client, "operator@example.com")
    product = create_catalog_product(db_session)

    entry = client.post(
        "/api/v1/movements/entries",
        headers=auth_header(token),
        json={"product_id": product.id, "quantity": "10.000", "note": "Entrada"},
    )
    exit_response = client.post(
        "/api/v1/movements/exits",
        headers=auth_header(token),
        json={"product_id": product.id, "quantity": "3.500"},
    )
    history = client.get("/api/v1/movements", headers=auth_header(token))

    assert entry.status_code == 201
    assert entry.json()["balance_before"] == "0.000"
    assert entry.json()["balance_after"] == "10.000"
    assert exit_response.status_code == 201
    assert exit_response.json()["quantity_delta"] == "-3.500"
    assert exit_response.json()["balance_after"] == "6.500"
    assert str(get_balance(db_session, product.id)) == "6.500"
    assert history.status_code == 200
    assert len(history.json()) == 2


def test_insufficient_balance_rejects_without_partial_change(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="operator@example.com", role=UserRole.OPERATOR)
    token = login(client, "operator@example.com")
    product = create_catalog_product(db_session)

    response = client.post(
        "/api/v1/movements/exits",
        headers=auth_header(token),
        json={"product_id": product.id, "quantity": "1.000"},
    )
    history = client.get("/api/v1/movements", headers=auth_header(token))

    assert response.status_code == 409
    assert str(get_balance(db_session, product.id)) == "0.000"
    assert history.json() == []


def test_adjustment_requires_manager_or_admin_and_reason(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="operator@example.com", role=UserRole.OPERATOR)
    create_test_user(db_session, email="manager@example.com", role=UserRole.MANAGER)
    operator_token = login(client, "operator@example.com")
    manager_token = login(client, "manager@example.com")
    product = create_catalog_product(db_session)

    operator_response = client.post(
        "/api/v1/movements/adjustments",
        headers=auth_header(operator_token),
        json={
            "product_id": product.id,
            "quantity_delta": "2.000",
            "reason": "Inventario",
        },
    )
    missing_reason = client.post(
        "/api/v1/movements/adjustments",
        headers=auth_header(manager_token),
        json={"product_id": product.id, "quantity_delta": "2.000", "reason": ""},
    )
    adjustment = client.post(
        "/api/v1/movements/adjustments",
        headers=auth_header(manager_token),
        json={
            "product_id": product.id,
            "quantity_delta": "2.000",
            "reason": "Inventario",
        },
    )

    assert operator_response.status_code == 403
    assert missing_reason.status_code == 422
    assert adjustment.status_code == 201
    assert adjustment.json()["reason"] == "Inventario"
    assert str(get_balance(db_session, product.id)) == "2.000"


def test_inactive_product_and_zero_quantity_are_rejected(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(db_session, email="admin@example.com", role=UserRole.ADMIN)
    token = login(client, "admin@example.com")
    product = create_catalog_product(db_session)
    product.is_active = False
    db_session.commit()

    inactive = client.post(
        "/api/v1/movements/entries",
        headers=auth_header(token),
        json={"product_id": product.id, "quantity": "1.000"},
    )
    zero = client.post(
        "/api/v1/movements/adjustments",
        headers=auth_header(token),
        json={
            "product_id": product.id,
            "quantity_delta": "0.000",
            "reason": "Inventario",
        },
    )

    assert inactive.status_code == 409
    assert zero.status_code == 422
