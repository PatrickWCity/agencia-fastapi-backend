from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    app_env: str = "local"

    admin_email: str
    items_per_user: int = 50

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
