from typing import Optional
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    name: str = Field(index=True, max_length=255, description="The name of the item")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    pass


class ItemPublic(ItemBase):
    id: int


class ItemUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
