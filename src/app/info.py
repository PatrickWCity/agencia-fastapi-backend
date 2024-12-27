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
        "app": {
            "name": settings.app_name,
            "env": settings.app_env,
        },
        "secret_key": settings.secret_key,
        "algorithm": settings.algorithm,
        "access_token_expire_minutes": settings.access_token_expire_minutes,
        "version": settings.version,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
        "camunda": {
            "url": settings.camunda_url,
            "user": settings.camunda_user,
            "password": settings.camunda_password,
            "tenant_id": settings.camunda_tenant_id or None,
        },
        "db": {
            "connection": settings.db_connection,
            "host": settings.db_host,
            "port": settings.db_port,
            "database": settings.db_database,
            "username": settings.db_username,
            "password": settings.db_password,
            "url": str(
                MultiHostUrl.build(
                    scheme=settings.db_connection,
                    host=settings.db_host,
                    port=settings.db_port or None,
                    path=settings.db_database,
                    username=settings.db_username,
                    password=settings.db_password,
                )
            ),
        },
    }
