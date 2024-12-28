from typing import TYPE_CHECKING, Optional, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.hero import Hero, HeroPublic


class TeamBase(SQLModel):
    name: str = Field(index=True, max_length=255)
    headquarters: str


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamPublic(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    headquarters: Optional[str] = None


class TeamPublicWithHeroes(TeamPublic):
    heroes: List["HeroPublic"] = []


# fix 'PydanticUndefinedAnnotation: name 'HeroPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.hero import HeroPublic

TeamPublicWithHeroes.model_rebuild()
