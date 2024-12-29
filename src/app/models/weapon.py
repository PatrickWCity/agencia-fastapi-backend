from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.hero import Hero, HeroPublic


class WeaponBase(SQLModel):
    name: str = Field(index=True, max_length=255, description="The name of the weapon")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The timestamp when the weapon was created",
    )
    updated_at: Optional[datetime] = Field(
        description="The timestamp when the weapon was updated"
    )
    deleted_at: Optional[datetime] = Field(
        description="The timestamp when the weapon was deleted"
    )


class Weapon(WeaponBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    heroes: Optional["Hero"] = Relationship(back_populates="weapon")


class WeaponPublic(WeaponBase):
    id: int


class WeaponCreate(WeaponBase):
    pass


class WeaponUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class WeaponPublicWithHeroes(WeaponPublic):
    heroes: List["HeroPublic"] = []


# fix 'PydanticUndefinedAnnotation: name 'HeroPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.hero import HeroPublic

WeaponPublicWithHeroes.model_rebuild()
