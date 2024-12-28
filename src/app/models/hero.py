from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.team import Team, TeamPublic


class HeroBase(SQLModel):
    name: str = Field(index=True, max_length=255, description="The name of the hero")
    secret_name: str = Field(max_length=255, description="The secret name of the hero")
    age: Optional[int] = Field(
        default=None, index=True, description="The age of the hero"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    team_id: Optional[int] = None


class HeroPublicWithTeam(HeroPublic):
    team: Optional["TeamPublic"] = None


# fix 'PydanticUndefinedAnnotation: name 'TeamPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.team import TeamPublic

HeroPublicWithTeam.model_rebuild()
