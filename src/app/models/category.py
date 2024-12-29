from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel


class CategoryBase(SQLModel):
    name: str = Field(
        index=True, max_length=255, description="The name of the category"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The timestamp when the category was created",
    )
    updated_at: Optional[datetime] = Field(
        description="The timestamp when the category was updated"
    )
    deleted_at: Optional[datetime] = Field(
        description="The timestamp when the category was deleted"
    )

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    category: Optional["Category"] = Relationship(
        sa_relationship_kwargs=dict(remote_side="Category.id")
    )
    categories: List["Category"] = Relationship(back_populates="category")


class CategoryPublic(CategoryBase):
    id: int


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    category_id: Optional[int] = None


class CategoryPublicWithCategory(CategoryPublic):
    category: Optional["CategoryPublic"] = None
    categories: List["CategoryPublic"] = []
