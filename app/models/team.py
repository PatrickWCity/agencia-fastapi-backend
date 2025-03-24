from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, timezone
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.hero import Hero, HeroPublic


class TeamBase(SQLModel):
    name: str = Field(index=True, max_length=255, description="The name of the team")
    headquarters: str = Field(
        max_length=255, description="The headquarters of the team"
    )
    created_at: SkipJsonSchema[datetime] = Field(
        default=datetime.now(timezone.utc),
        description="The timestamp when the team was created",
    )
    updated_at: SkipJsonSchema[Optional[datetime]] = Field(
        default=None, description="The timestamp when the team was updated"
    )
    deleted_at: SkipJsonSchema[Optional[datetime]] = Field(
        default=None, description="The timestamp when the team was deleted"
    )


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamPublic(TeamBase):
    id: int


class TeamCreate(TeamBase):
    pass


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
