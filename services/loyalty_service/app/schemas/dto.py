from pydantic import BaseModel


class LoyaltyInfoResponse(BaseModel):
    status: str
    discount: int
    reservationCount: int


class LoyaltyInfoRequest(BaseModel):
    reservationCountOperation: int | None = None
