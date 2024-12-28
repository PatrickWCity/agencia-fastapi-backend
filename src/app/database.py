from pydantic_core import MultiHostUrl
from sqlmodel import Session, SQLModel, create_engine

from app.config import settings

db_url = str(
    MultiHostUrl.build(
        scheme=settings.db_connection,
        host=settings.db_host,
        port=settings.db_port or None,
        path=settings.db_database,
        username=settings.db_username,
        password=settings.db_password,
    )
)

engine = create_engine(db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
