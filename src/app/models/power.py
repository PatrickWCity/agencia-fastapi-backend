from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.hero import Hero, HeroPublic


class PowerBase(SQLModel):
    name: str = Field(index=True, max_length=255, description="The name of the power")
    created_at: SkipJsonSchema[datetime] = Field(
        default=datetime.now(timezone.utc),
        description="The timestamp when the power was created",
    )
    updated_at: SkipJsonSchema[Optional[datetime]] = Field(
        default=None, description="The timestamp when the power was updated"
    )
    deleted_at: SkipJsonSchema[Optional[datetime]] = Field(
        default=None, description="The timestamp when the power was deleted"
    )

    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id")


class Power(PowerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    hero: Optional["Hero"] = Relationship(back_populates="powers")


class PowerPublic(PowerBase):
    id: int


class PowerCreate(PowerBase):
    pass


class PowerUpdate(SQLModel):
    name: Optional[str] = None

    hero_id: Optional[int] = None


class PowerPublicWithHero(PowerPublic):
    hero: Optional["HeroPublic"] = None


# fix 'PydanticUndefinedAnnotation: name 'HeroPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.hero import HeroPublic

PowerPublicWithHero.model_rebuild()
