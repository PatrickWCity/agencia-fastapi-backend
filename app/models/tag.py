from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, timezone
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.item import Item, ItemPublic


class TagBase(SQLModel):
    name: str = Field(index=True, max_length=255, description="The name of the tag")
    created_at: SkipJsonSchema[datetime] = Field(
        default=datetime.now(timezone.utc),
        description="The timestamp when the tag was created",
    )
    updated_at: SkipJsonSchema[Optional[datetime]] = Field(
        default=None, description="The timestamp when the tag was updated"
    )
    deleted_at: SkipJsonSchema[Optional[datetime]] = Field(
        default=None, description="The timestamp when the tag was deleted"
    )


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    items: List["Item"] = Relationship(back_populates="tag")


class TagPublic(TagBase):
    id: int


class TagCreate(TagBase):
    pass


class TagUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None


class TagPublicWithItems(TagPublic):
    items: List["ItemPublic"] = []


# fix 'PydanticUndefinedAnnotation: name 'ItemPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.item import ItemPublic

TagPublicWithItems.model_rebuild()
