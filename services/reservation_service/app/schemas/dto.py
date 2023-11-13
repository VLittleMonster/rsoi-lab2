from pydantic import BaseModel, validator
from typing import Literal, Annotated, List, Optional
from uuid import UUID
from datetime import datetime, date

class HotelInfo(BaseModel):
    hotelUid: UUID
    name: str
    fullAddress: str
    stars: int

class HotelResponse(BaseModel):
    hotelUid: UUID
    name: str
    country: str
    city: str
    address: str
    stars: int
    price: float

class PaginationResponse(BaseModel):
    page: int
    pageSize: int
    totalElements: int
    items: List[HotelResponse]


class ReservationResponse(BaseModel):
    reservationUid: UUID
    hotel: HotelInfo
    startDate: date
    endDate: date
    status: Literal['PAID', 'CANCELED']
    paymentUid: UUID


class CreateReservationRequest(BaseModel):
    paymentUid: UUID
    hotelUid: UUID
    startDate: date
    endDate: date

    @validator("startDate", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()

    @validator("endDate", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()
    
class CreateReservationResponse(BaseModel):
    reservationUid: UUID
    paymentUid: UUID
    hotelUid: UUID
    startDate: date
    endDate: date
    status: Literal['PAID', 'CANCELED']

class UpdateReservation(BaseModel):
    paymentUid: Optional[UUID] = None
    hotelUid: Optional[UUID] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    status: Optional[Literal['PAID', 'CANCELED']] = None

    @validator("startDate", pre=True)
    def parse_date(cls, value):
        if value is None:
            return None
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()

    @validator("endDate", pre=True)
    def parse_date(cls, value):
        if value is None:
            return None
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()
