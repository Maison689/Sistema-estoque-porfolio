import os

from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models.user import UserRole
from app.schemas.user import UserCreate
from app.services.users import create_user, get_user_by_email


def main() -> None:
    email = os.environ["ADMIN_INITIAL_EMAIL"]
    password = os.environ["ADMIN_INITIAL_PASSWORD"]
    name = os.environ.get("ADMIN_INITIAL_NAME", "Administrador")

    with SessionLocal() as db:
        existing = get_user_by_email(db, email)
        if existing is not None:
            print("Initial admin already exists.")
            return

        try:
            create_user(
                db,
                UserCreate(
                    name=name,
                    email=email,
                    password=password,
                    role=UserRole.ADMIN,
                    is_active=True,
                ),
            )
        except IntegrityError:
            db.rollback()
            print("Initial admin already exists.")
            return

    print("Initial admin created.")


if __name__ == "__main__":
    main()
