from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models.item import (
    Item,
    ItemCreate,
    ItemPublic,
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
    items = session.exec(select(Item).offset(offset).limit(limit)).all()
    return items


@router.get("/items/{item_id}", response_model=ItemPublic, tags=["items"])
def read_item(*, item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
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
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/items/{item_id}", tags=["items"])
def delete_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
