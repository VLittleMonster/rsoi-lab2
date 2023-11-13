from sqlalchemy import Integer, Column, VARCHAR
from typing import Final, Any
from database.database import Base
from schemas.dto import LoyaltyInfoResponse

DISCOUNT_BY_STATUS: Final = {'BRONZE': 5, 'SILVER': 7, 'GOLD': 10}  # статусы и размеры скидок в процентах


class Loyalty(Base):
    __tablename__ = 'loyalty'
    __table_args__ = {
        'extend_existing': True
    }

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(80), nullable=False, unique=True)
    __reservation_count = Column(Integer, nullable=False, default=0, name='reservation_count')
    __status = Column(VARCHAR(80), nullable=False, default=list(DISCOUNT_BY_STATUS.keys())[0], name='status')
    __discount = Column(Integer, nullable=False, default=int(DISCOUNT_BY_STATUS[list(DISCOUNT_BY_STATUS.keys())[0]]), name='discount')

    def __init__(self, name):
        self.username = name

    def get_dto_model(self):
        return LoyaltyInfoResponse(
            status=self.__status,
            discount=self.__discount,
            reservationCount=self.__reservation_count
        )

    def update_reservation_count(self, reservation_count_operation: int):
        if reservation_count_operation > 0:
            self.__reservation_count += 1
        else:
            self.__reservation_count = max(self.__reservation_count - 1, 0)
        self.__status = self.get_status_by_reservation_count(self.__reservation_count)
        self.__discount = DISCOUNT_BY_STATUS[self.__status]

    @staticmethod
    def get_status_by_reservation_count(reservation_count) -> str:
        return list(DISCOUNT_BY_STATUS.keys())[min(reservation_count % 100 // 10, 2)]
