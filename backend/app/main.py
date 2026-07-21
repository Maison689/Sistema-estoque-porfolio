from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import (
    auth,
    categories,
    health,
    movements,
    products,
    suppliers,
    users,
)
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router, prefix=settings.api_v1_prefix)
    app.include_router(categories.router, prefix=settings.api_v1_prefix)
    app.include_router(health.router, prefix=settings.api_v1_prefix)
    app.include_router(movements.router, prefix=settings.api_v1_prefix)
    app.include_router(products.router, prefix=settings.api_v1_prefix)
    app.include_router(suppliers.router, prefix=settings.api_v1_prefix)
    app.include_router(users.router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
