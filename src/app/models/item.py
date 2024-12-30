from typing import Optional
from datetime import datetime, timezone
from pydantic.json_schema import SkipJsonSchema


class ItemBase(SQLModel):
    name: str = Field(index=True, max_length=255, description="The name of the item")
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


class ItemPublic(ItemBase):
    id: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None


