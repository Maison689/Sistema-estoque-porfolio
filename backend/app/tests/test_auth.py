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


def create_test_user(
    db: Session,
    *,
    email: str,
    password: str,
    role: UserRole,
    is_active: bool = True,
):
    return create_user(
        db,
        UserCreate(
            name="Test User",
            email=email,
            password=password,
            role=role,
            is_active=is_active,
        ),
    )


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_login_and_me_do_not_return_password(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(
        db_session,
        email="admin@example.com",
        password="strong-password",
        role=UserRole.ADMIN,
    )

    token = login(client, "ADMIN@example.com", "strong-password")
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "admin@example.com"
    assert body["role"] == "ADMIN"
    assert "password" not in body
    assert "password_hash" not in body


def test_invalid_credentials_and_inactive_user_are_rejected(
    client: TestClient,
    db_session: Session,
) -> None:
    create_test_user(
        db_session,
        email="inactive@example.com",
        password="strong-password",
        role=UserRole.OPERATOR,
        is_active=False,
    )

    invalid = client.post(
        "/api/v1/auth/login",
        json={"email": "missing@example.com", "password": "wrong"},
    )
    inactive = client.post(
        "/api/v1/auth/login",
        json={"email": "inactive@example.com", "password": "strong-password"},
    )

    assert invalid.status_code == 401
    assert inactive.status_code == 401


def test_only_admin_can_manage_users(client: TestClient, db_session: Session) -> None:
    create_test_user(
        db_session,
        email="admin@example.com",
        password="strong-password",
        role=UserRole.ADMIN,
    )
    create_test_user(
        db_session,
        email="operator@example.com",
        password="strong-password",
        role=UserRole.OPERATOR,
    )

    admin_token = login(client, "admin@example.com", "strong-password")
    operator_token = login(client, "operator@example.com", "strong-password")

    admin_response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    operator_response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {operator_token}"},
    )

    assert admin_response.status_code == 200
    assert operator_response.status_code == 403
