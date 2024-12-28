from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.hero import Hero, HeroPublic


class TeamBase(SQLModel):
    name: str = Field(index=True, max_length=255, description="The name of the team")
    headquarters: str = Field(
        max_length=255, description="The headquarters of the team"
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class TeamPublicWithHeroes(TeamPublic):
    heroes: List["HeroPublic"] = []


# fix 'PydanticUndefinedAnnotation: name 'HeroPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.hero import HeroPublic

TeamPublicWithHeroes.model_rebuild()
