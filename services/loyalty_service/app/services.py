from models import Loyalty
from sqlalchemy.orm import Session
from schemas.dto import LoyaltyInfoRequest
from fastapi import status
from fastapi.exceptions import HTTPException


async def get_loyalty(username: str, db: Session):
    client = db.query(Loyalty).filter(Loyalty.username == username).first()
    if client is None:
        client = await create_loyalty(username, db)
    return client


async def create_loyalty(username: str, db: Session) -> Loyalty:
    new_client = Loyalty(name=username)
    try:
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
    except Exception as e:
        print(e)

    return new_client


async def update_loyalty(data: LoyaltyInfoRequest, username: str, db: Session) -> Loyalty:
    loyalty = db.query(Loyalty).filter(Loyalty.username == username).first()

    if loyalty is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if data.reservationCountOperation:
        loyalty.update_reservation_count(data.reservationCountOperation)
    db.add(loyalty)
    db.commit()
    db.refresh(loyalty)

    return loyalty
