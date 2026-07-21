from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import CurrentUser, DbSession
from app.core.security import create_access_token
from app.schemas.auth import CurrentUserResponse, LoginRequest, TokenResponse
from app.services.users import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: DbSession) -> TokenResponse:
    user = authenticate_user(db, payload.email, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    token = create_access_token(
        subject=str(user.id),
        extra_claims={"role": user.role.value},
    )
    return TokenResponse(access_token=token)


@router.get("/me", response_model=CurrentUserResponse)
def read_me(current_user: CurrentUser) -> CurrentUserResponse:
    return CurrentUserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active,
    )


@router.post("/logout")
def logout() -> dict[str, str]:
    return {"status": "ok"}
