from enum import Enum
from models import Hotel as HotelModel
from models import Reservation as ReservationModel
from schemas.dto import HotelInfo
from schemas.dto import HotelResponse
from schemas.dto import PaginationResponse
from schemas.dto import ReservationResponse
from schemas.dto import CreateReservationResponse
from schemas.dto import UpdateReservation

class ResponsesEnum(Enum):
    HotelInfo = {
        "model": HotelInfo
    }

    HotelResponse = {
        "model": HotelResponse
    }

    PaginationResponse = {
        "model": PaginationResponse
    }

    ReservationResponse = {
        "model": ReservationResponse
    }

    CreateReservationResponse = {
        "model": CreateReservationResponse
    }

    UpdateReservation = {
        "model": UpdateReservation
    }

    @staticmethod
    def get_hotel_response(Hotel: HotelModel):
        return HotelModel.get_hotel_response(Hotel)
    
    @staticmethod
    def get_reservation_response(Reservation: ReservationModel):
        return ReservationModel.get_dto_model(Reservation)
