from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, timezone
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import Field, Relationship, SQLModel

from app.models.user_item import User_Item

if TYPE_CHECKING:
    from app.models.tag import Tag, TagPublic
    from app.models.user import User, UserPublic


class ItemBase(SQLModel):
    name: str = Field(index=True, max_length=255, description="The name of the item")
    description: Optional[str] = Field(
        default=None, title="The description of the item", max_length=255
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Optional[float] = Field(default=19.0)
    created_at: SkipJsonSchema[datetime] = Field(
        default=datetime.now(timezone.utc),
        description="The timestamp when the item was created",
    )
    updated_at: SkipJsonSchema[Optional[datetime]] = Field(
        default=None, description="The timestamp when the item was updated"
    )
    deleted_at: SkipJsonSchema[Optional[datetime]] = Field(
        default=None, description="The timestamp when the item was deleted"
    )


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tags: List["Tag"] = Relationship(back_populates="item")
    users: List["User_Item"] = Relationship(back_populates="item", link_model=User_Item)


class ItemPublic(ItemBase):
    id: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None


class ItemPublicWithTagsUsers(ItemPublic):
    tags: List["TagPublic"] = []
    users: List["UserPublic"] = []


# fix 'PydanticUndefinedAnnotation: name 'TagPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.tag import TagPublic

# fix 'PydanticUndefinedAnnotation: name 'UserPublic' is not defined' error
# see: https://github.com/tiangolo/sqlmodel/discussions/757
from app.models.user import UserPublic

ItemPublicWithTagsUsers.model_rebuild()
