from enum import Enum
from models import Loyalty as LoyaltyModel
from schemas.dto import LoyaltyInfoResponse


class ResponsesEnum(Enum):
    LoyaltyInfoResponse = {
        "model": LoyaltyInfoResponse
    }

    LoyaltyUpdateResponse = {
        "description": "info was updated"
    }

    @staticmethod
    def get_loyalty_response(loyalty: LoyaltyModel):
        return LoyaltyModel.get_dto_model(loyalty)
