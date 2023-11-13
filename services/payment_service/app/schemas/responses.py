from enum import Enum
from models import Payment as PaymentModel
from schemas.dto import PaymentInfo
from typing import List


class ResponsesEnum(Enum):
    PaymentInfo = {
        "model": PaymentInfo
    }

    """PaymentInfoArray = {
        "model": List[PaymentInfo]
    }"""

    PaymentUpdateResponse = {
        "description": "info was updated"
    }

    @staticmethod
    def get_payment_response(Payment: PaymentModel):
        return PaymentModel.get_dto_model(Payment)
