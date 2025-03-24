from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.item import Item
    from app.models.user import User


class User_ItemBase(SQLModel):
    created_at: SkipJsonSchema[datetime] = Field(
        default=datetime.now(timezone.utc),
        description="The timestamp when the user item was created",
    )
    is_training: bool = False


class User_Item(User_ItemBase, table=True):
    item_id: Optional[int] = Field(
        default=None, foreign_key="item.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    item: "Item" = Relationship(back_populates="users")
    user: "User" = Relationship(back_populates="items")
