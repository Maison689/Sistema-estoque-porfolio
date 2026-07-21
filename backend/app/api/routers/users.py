from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import DbSession, require_roles
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.users import create_user, get_user_by_id, list_users, update_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)


@router.get("", response_model=list[UserResponse])
def read_users(db: DbSession) -> list[User]:
    return list_users(db)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(payload: UserCreate, db: DbSession) -> User:
    try:
        return create_user(db, payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail already exists.",
        ) from exc


@router.patch("/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, payload: UserUpdate, db: DbSession) -> User:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return update_user(db, user, payload)
