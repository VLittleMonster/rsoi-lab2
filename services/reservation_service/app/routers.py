from fastapi import APIRouter, Depends, status, Header, Response, Request
from sqlalchemy.orm import Session
from database.AppDatabase import AppDatabase
from config.config import get_settings

import services as ReservationService
from schemas.responses import ResponsesEnum
from schemas.dto import UpdateReservation
from schemas.dto import CreateReservationRequest
from uuid import UUID

router = APIRouter(prefix='', tags=['Reservation REST API operations'])
app_db = AppDatabase.app_db
settings = get_settings()


@router.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_availability():
    return Response(status_code=status.HTTP_200_OK)


@router.get(f'{settings["prefix"]}/hotels', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.PaginationResponse.value
            })
async def get_hotels(page: int = 0, size: int = 0, db: Session = Depends(app_db.get_db)):
    hotels = await ReservationService.get_hotels(page, size, db)
    return hotels


@router.get(f'{settings["prefix"]}/hotels/' + '{hotelUid}', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.HotelResponse.value
            })
async def get_hotel(hotelUid: UUID, db: Session = Depends(app_db.get_db)):
    hotel = await ReservationService.get_hotel(hotelUid, db)
    return ResponsesEnum.get_hotel_response(hotel)


@router.get(f'{settings["prefix"]}/reservations', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationResponse.value
            })
async def get_reservations(username: str = Header(alias='X-User-Name'), db: Session = Depends(app_db.get_db)):
    reservations = await ReservationService.get_reservations(username, db)
    return reservations


@router.get(f'{settings["prefix"]}/reservations/' + '{reservationUid}', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationResponse.value
            })
async def get_reservation(reservationUid: UUID, username: str = Header(alias='X-User-Name'), db: Session = Depends(app_db.get_db)):
    reservation = await ReservationService.get_reservation(reservationUid, username, db)
    return reservation


@router.post(f'{settings["prefix"]}/reservations', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.CreateReservationResponse.value
            })
async def create_reservation(username: str = Header(alias='X-User-Name'), data: CreateReservationRequest = None, db: Session = Depends(app_db.get_db)):
    reservation = await ReservationService.create_reservation(username, data, db)
    return reservation


@router.patch(f'{settings["prefix"]}/reservations/' + '{reservationUid}', status_code=status.HTTP_200_OK,
              responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationResponse.value
              })
async def update_reservation(reservationUid: UUID, data: UpdateReservation = None, username: str = Header(alias='X-User-Name'), db: Session = Depends(app_db.get_db)):
    reservation = await ReservationService.update_reservation(reservationUid, data, username, db)
    return reservation.model_dump()
