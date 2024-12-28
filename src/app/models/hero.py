from typing import TYPE_CHECKING, Optional, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.team import Team, TeamPublic


class HeroBase(SQLModel):
    name: str = Field(index=True, max_length=255)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    team: Optional["Team"] = Relationship(back_populates="heroes")


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    pass


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None


class HeroPublicWithTeam(HeroPublic):
    team: Optional["TeamPublic"] = None


# fix 'PydanticUndefinedAnnotation: name 'TeamPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.team import TeamPublic

HeroPublicWithTeam.model_rebuild()
