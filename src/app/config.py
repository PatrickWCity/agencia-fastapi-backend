from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    app_env: str = "local"

    admin_email: str
    items_per_user: int = 50
    version: str = "0.1.0"

    camunda_url: str = "http://localhost:8080/engine-rest"
    camunda_user: str = "demo"
    camunda_password: str = "demo"
    camunda_tenant_id: int = None

    db_connection: str = "sqlite"
    db_host: str = ""
    db_port: int = None
    db_database: str = "/database.db"
    db_username: str = ""
    db_password: str = ""

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env.local", ".env"),
        extra="ignore",
    )
