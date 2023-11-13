from enum import Enum
from schemas import dto as schemas


class ResponsesEnum(Enum):
    LoyaltyInfoResponse = {
        "model": schemas.LoyaltyInfoResponse
    }

    HotelInfo = {
        "model": schemas.HotelInfo
    }

    HotelResponse = {
        "model": schemas.HotelResponse
    }

    PaginationResponse = {
        "model": schemas.PaginationResponse
    }

    PaymentInfo = {
        "model": schemas.PaymentInfo
    }

    CreateReservationRequest = {
        "model": schemas.CreateReservationRequest
    }

    CreateReservationResponse = {
        "model": schemas.CreateReservationResponse
    }

    ReservationsResponse = {
        "model": list[schemas.ReservationResponse]
    }

    ReservationResponse = {
        "model": schemas.ReservationResponse
    }

    UserInfoResponse = {
        "model": schemas.UserInfoResponse
    }

    ErrorResponse = {
        "model": schemas.ErrorResponse
    }

    ErrorDescription = {
        "model": schemas.ErrorDescription
    }

    ValidationErrorResponse = {
        "model": schemas.ValidationErrorResponse
    }
