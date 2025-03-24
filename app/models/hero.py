from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, timezone
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.power import Power, PowerPublic
    from app.models.team import Team, TeamPublic
    from app.models.weapon import Weapon, WeaponPublic


class HeroBase(SQLModel):
    name: str = Field(index=True, max_length=255, description="The name of the hero")
    secret_name: str = Field(max_length=255, description="The secret name of the hero")
    age: Optional[int] = Field(
        default=None, index=True, description="The age of the hero"
    )
    created_at: SkipJsonSchema[datetime] = Field(
        default=datetime.now(timezone.utc),
        description="The timestamp when the hero was created",
    )
    updated_at: SkipJsonSchema[Optional[datetime]] = Field(
        default=None, description="The timestamp when the hero was updated"
    )
    deleted_at: SkipJsonSchema[Optional[datetime]] = Field(
        default=None, description="The timestamp when the hero was deleted"
    )

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    weapon_id: Optional[int] = Field(default=None, foreign_key="weapon.id")


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    team: Optional["Team"] = Relationship(back_populates="heroes")

    weapon: Optional["Weapon"] = Relationship(back_populates="heroes")

    powers: List["Power"] = Relationship(back_populates="hero")


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    pass


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None

    team_id: Optional[int] = None
    weapon_id: Optional[int] = None


class HeroPublicWithPowersTeamWeapon(HeroPublic):
    team: Optional["TeamPublic"] = None
    weapon: Optional["WeaponPublic"] = None
    powers: List["PowerPublic"] = []


# fix 'PydanticUndefinedAnnotation: name 'PowerPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.power import PowerPublic

# fix 'PydanticUndefinedAnnotation: name 'TeamPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.team import TeamPublic

# fix 'PydanticUndefinedAnnotation: name 'WeaponPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.weapon import WeaponPublic

HeroPublicWithPowersTeamWeapon.model_rebuild()
