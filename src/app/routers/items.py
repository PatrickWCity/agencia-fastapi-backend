from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.database import get_session
from app.models.item import (
    Item,
    ItemCreate,
    ItemPublic,
    ItemPublicWithUsers,
    ItemUpdate,
)

router = APIRouter()


@router.post("/items/", response_model=ItemPublic, tags=["items"])
def create_item(*, session: Session = Depends(get_session), item: ItemCreate):
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.get("/items/", response_model=list[ItemPublic], tags=["items"])
def read_items(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    items = session.exec(
        select(Item).where(Item.deleted_at == None).offset(offset).limit(limit)
    ).all()
    return items


@router.get("/items/{item_id}", response_model=ItemPublicWithUsers, tags=["items"])
def read_item(*, item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item or item.deleted_at != None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/items/{item_id}", response_model=ItemPublic, tags=["items"])
def update_item(
    *,
    session: Session = Depends(get_session),
    item_id: int,
    item: ItemUpdate,
):
    db_item = session.get(Item, item_id)
    if not db_item or db_item.deleted_at != None:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    db_item.updated_at = datetime.now(timezone.utc)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/items/{item_id}", tags=["items"])
def delete_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item or item.deleted_at != None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.deleted_at = datetime.now(timezone.utc)
    item.users.clear()
    session.add(item)
    session.commit()
    return {"ok": True}
