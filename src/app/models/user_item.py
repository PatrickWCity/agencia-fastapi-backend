from datetime import datetime, timezone
from typing import Optional
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import Field, SQLModel


class User_ItemBase(SQLModel):
    created_at: SkipJsonSchema[datetime] = Field(
        default=datetime.now(timezone.utc),
        description="The timestamp when the user item was created",
    )


class User_Item(User_ItemBase, table=True):
    item_id: Optional[int] = Field(
        default=None, foreign_key="item.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
