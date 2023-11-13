from models import Reservation
from models import Hotel
from sqlalchemy.orm import Session
from schemas.dto import UpdateReservation
from schemas.dto import PaginationResponse
from schemas.dto import CreateReservationRequest
from schemas.dto import CreateReservationResponse
from fastapi import status
from fastapi.exceptions import HTTPException
from uuid import UUID

async def get_hotels(page: int, size: int, db: Session):
    hotels = list(db.query(Hotel).all())
    hotel_resp = []
    for hotel in hotels:
        hotel_resp.append(hotel.get_hotel_response())

    if size == 0 and page == 0:
        return PaginationResponse(
            page = page,
            pageSize = size,
            totalElements = len(hotels),
            items = hotel_resp
        )
    size = max(1, size)
    size = min(100, size)
    page = max(1, page)

    l = min((page - 1)*size, len(hotels) - 1)
    r = min(l + size, len(hotels))

    request_hotels = hotel_resp[l:r]
    
    return PaginationResponse(page = page,
                              pageSize = r-l,
                              totalElements = len(hotels),
                              items = request_hotels)#.model_dump()


async def get_hotel(hotelUid: UUID, db: Session) -> Hotel:
    hotels = list(db.query(Hotel).all())
    hotel = None
    for h in hotels:
        if h.hotel_uid == hotelUid:
            hotel = h
            break

    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return hotel

async def get_reservations(username: str, db: Session):
    reservations = db.query(Reservation).filter(Reservation.username == username).all()

    if reservations is None or len(reservations) == 0:
        return []

    result_reservations = []

    for reservation in reservations:
        result_reservations.append(reservation.get_dto_model(db))

    return result_reservations

async def get_reservation(reservationUid: UUID, username: str, db: Session):
    reservation = db.query(Reservation).filter(Reservation.reservation_uid == reservationUid, Reservation.username == username).first()

    if reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return reservation.get_dto_model(db)

async def create_reservation(username: str, data: CreateReservationRequest, db: Session):
    try:
        hotel = await get_hotel(data.hotelUid, db)
        new_reservation = Reservation(
                    username = username,
                    payment_uid = data.paymentUid,
                    hotel_id = hotel.id,
                    start_date = data.startDate,
                    end_date = data.endDate
        )

        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)
        return new_reservation.get_created_reservation(db)
    except HTTPException as exc:
        print(exc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def update_reservation(reservationUid: UUID, data: UpdateReservation, username: str, db: Session):
    reservation = db.query(Reservation).filter(Reservation.reservation_uid == reservationUid, Reservation.username == username).first()
    
    if reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if data.status:
        reservation.update_reservation_status(data.status)

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return reservation.get_updated_reservation(db)
