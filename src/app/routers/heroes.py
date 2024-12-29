from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.database import get_session
from app.models.hero import Hero, HeroCreate, HeroPublic, HeroPublicWithTeam, HeroUpdate

router = APIRouter()


@router.post("/heroes/", response_model=HeroPublic, tags=["heroes"])
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.get("/heroes/", response_model=list[HeroPublic], tags=["heroes"])
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    heroes = session.exec(
        select(Hero).where(Hero.deleted_at == None).offset(offset).limit(limit)
    ).all()
    return heroes


@router.get("/heroes/{hero_id}", response_model=HeroPublicWithTeam, tags=["heroes"])
def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero or hero.deleted_at != None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.patch("/heroes/{hero_id}", response_model=HeroPublic, tags=["heroes"])
def update_hero(
    *, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate
):
    db_hero = session.get(Hero, hero_id)
    if not db_hero or db_hero.deleted_at != None:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    db_hero.updated_at = datetime.now(timezone.utc)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.delete("/heroes/{hero_id}", tags=["heroes"])
def delete_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero or hero.deleted_at != None:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero.deleted_at = datetime.now(timezone.utc)
    session.add(hero)
    session.commit()
    return {"ok": True}
