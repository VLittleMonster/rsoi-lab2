from pydantic import BaseModel, validator
from typing import Literal, Annotated, List
from uuid import UUID
from datetime import datetime, date


class LoyaltyInfoResponse(BaseModel):
    status: Literal['BRONZE', 'SILVER', 'GOLD']
    discount: int
    reservationCount: int


class LoyaltyInfoRequest(BaseModel):
    reservationCountOperation: int | None = None


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


class PaymentInfo(BaseModel):
    status: Literal['PAID', 'CANCELED']
    price: int


class PaymentInfoResponse(BaseModel):
    status: Literal['PAID', 'CANCELED']
    price: int
    uid: UUID


class UpdatePaymentRequest(BaseModel):
    status: Literal['PAID', 'CANCELED'] | None = None
    price: int | None = None


class CreateReservationRequest(BaseModel):
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
    hotelUid: UUID
    startDate: date
    endDate: date
    discount: int
    status: Literal['PAID', 'CANCELED']
    payment: PaymentInfo

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


class ReservationResponse(BaseModel):
    reservationUid: UUID
    hotel: HotelInfo
    startDate: date
    endDate: date
    status: Literal['PAID', 'CANCELED']
    payment: PaymentInfo

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


class UserInfoResponse(BaseModel):
    reservations: List[ReservationResponse]
    loyalty: LoyaltyInfoResponse


class ErrorResponse(BaseModel):
    message: str = 'not found'


class ErrorDescription(BaseModel):
    field: str
    error: str


class ValidationErrorResponse(BaseModel):
    message: str
    errors: List[ErrorDescription]


class CreateReservationRequestForReservService(BaseModel):
    paymentUid: UUID
    hotelUid: UUID
    startDate: date
    endDate: date


class UpdateReservationRequestForReservService(BaseModel):
    paymentUid: UUID | None = None
    hotelUid: UUID | None = None
    startDate: date | None = None
    endDate: date | None = None
    status: Literal['PAID', 'CANCELED'] | None = None


class UpdateReservationResponseFromReservService(BaseModel):
    paymentUid: UUID
    hotelUid: UUID
    startDate: date
    endDate: date
    status: Literal['PAID', 'CANCELED']

    @validator("startDate", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%d/%m/%Y"
        ).date()


class CreateReservationResponseFromReservService(BaseModel):
    reservationUid: UUID
    paymentUid: UUID
    hotelUid: UUID
    startDate: date
    endDate: date
    status: Literal['PAID', 'CANCELED']

    @validator("startDate", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%d/%m/%Y"
        ).date()


class ReservationResponseFromReservService(BaseModel):
    reservationUid: UUID
    hotel: HotelInfo
    startDate: date
    endDate: date
    status: Literal['PAID', 'CANCELED']
    paymentUid: UUID

    @validator("startDate", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%d/%m/%Y"
        ).date()
