from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from pydantic_core import MultiHostUrl

from .config import Settings

app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "app_env": settings.app_env,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
        "db_connection": settings.db_connection,
        "db_host": settings.db_host,
        "db_port": settings.db_port,
        "db_database": settings.db_database,
        "db_username": settings.db_username,
        "db_password": settings.db_password,
        "db_url": str(
            MultiHostUrl.build(
                scheme=settings.db_connection,
                host=settings.db_host,
                port=settings.db_port or None,
                path=settings.db_database,
                username=settings.db_username,
                password=settings.db_password,
            )
        ),
    }
