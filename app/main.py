from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI

from app.dependencies import get_query_token, get_token_header
from app.internal import admin
from app.routers import categories, heroes, items, powers, tags, teams, users, weapons

from app.database import create_db_and_tables
from app.models.category import Category
from app.models.hero import Hero
from app.models.item import Item
from app.models.power import Power
from app.models.tag import Tag
from app.models.team import Team
from app.models.user import User
from app.models.user_item import User_Item
from app.models.weapon import Weapon


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(dependencies=[Depends(get_query_token)], lifespan=lifespan)

app.include_router(categories.router)
app.include_router(heroes.router)
app.include_router(items.router)
app.include_router(powers.router)
app.include_router(tags.router)
app.include_router(teams.router)
app.include_router(users.router)
app.include_router(weapons.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
