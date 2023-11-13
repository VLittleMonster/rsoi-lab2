from sqlalchemy import Integer, Column, VARCHAR, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from typing import Final, Any
from database.database import Base
from schemas.dto import PaymentInfo
import uuid

PAYMENT_STATUS: Final = ['CANCELED', 'PAID']

class Payment(Base):
    __tablename__ = 'payment'
    __table_args__ = {
        'extend_existing': True,
        # 'CheckConstraint': CheckConstraint(f'CHECK (status in {str(list(DISCOUNT_BY_STATUS.keys()))})')
    }

    id = Column(Integer, primary_key=True)
    payment_uid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4, unique=True)
    __status = Column(VARCHAR(20), nullable=False, default='PAID')
    __price = Column(Integer, nullable=False)

    def __init__(self, payment_price):
        self.__price = payment_price

    def get_dto_model(self):
        return self.get_payment_info().model_dump()

    def get_payment_info(self):
        return PaymentInfo(
            status=self.__status,
            price=self.__price,
            uid=self.payment_uid
        )

    def update_payment_status(self, new_payment_status: str):
        self.__status = new_payment_status

    def update_payment_price(self, new_payment_price: int):
        self.__price = new_payment_price
