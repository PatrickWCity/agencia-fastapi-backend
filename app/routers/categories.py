from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.database import get_session
from app.models.category import (
    Category,
    CategoryCreate,
    CategoryPublic,
    CategoryPublicWithCategory,
    CategoryUpdate,
)

router = APIRouter()


@router.post("/categories/", response_model=CategoryPublic, tags=["categories"])
def create_category(
    *, session: Session = Depends(get_session), category: CategoryCreate
):
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.get("/categories/", response_model=list[CategoryPublic], tags=["categories"])
def read_categories(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    categories = session.exec(
        select(Category).where(Category.deleted_at == None).offset(offset).limit(limit)
    ).all()
    return categories


@router.get(
    "/categories/{category_id}",
    response_model=CategoryPublicWithCategory,
    tags=["categories"],
)
def read_category(*, session: Session = Depends(get_session), category_id: int):
    category = session.get(Category, category_id)
    if not category or category.deleted_at != None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch(
    "/categories/{category_id}", response_model=CategoryPublic, tags=["categories"]
)
def update_category(
    *,
    session: Session = Depends(get_session),
    category_id: int,
    category: CategoryUpdate,
):
    db_category = session.get(Category, category_id)
    if not db_category or db_category.deleted_at != None:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category.model_dump(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    db_category.updated_at = datetime.now(timezone.utc)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.delete("/categories/{category_id}", tags=["categories"])
def delete_category(*, session: Session = Depends(get_session), category_id: int):
    category = session.get(Category, category_id)
    if not category or category.deleted_at != None:
        raise HTTPException(status_code=404, detail="Category not found")
    category.deleted_at = datetime.now(timezone.utc)
    if category.category:
        if category.category.category_id == category_id:
            category.category.category_id = None
            category.category.updated_at = datetime.now(timezone.utc)
    for db_category in category.categories:
        db_category.updated_at = datetime.now(timezone.utc)
        session.add(db_category)
    category.categories.clear()
    session.add(category)
    session.commit()
    return {"ok": True}
