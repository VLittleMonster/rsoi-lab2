from sqlalchemy import Integer, Column, VARCHAR, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base
from schemas.dto import HotelInfo
from schemas.dto import HotelResponse
from schemas.dto import ReservationResponse
from schemas.dto import CreateReservationResponse
import uuid
from sqlalchemy.orm import Session

class Hotel(Base):
    __tablename__ = 'hotels'
    __table_args__ = {
        'extend_existing': True,
        # 'CheckConstraint': CheckConstraint(f'CHECK (status in {str(list(DISCOUNT_BY_STATUS.keys()))})')
    }

    id = Column(Integer, primary_key=True)
    hotel_uid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4, unique=True)
    name = Column(VARCHAR(255), nullable=False)
    country = Column(VARCHAR(80), nullable=False)
    city = Column(VARCHAR(80), nullable=False)
    adress = Column(VARCHAR(255), nullable=False)
    stars = Column(Integer)
    price = Column(Integer, nullable=False)

    def get_hotel_info(self):
        return HotelInfo(
            hotelUid=self.hotel_uid,
            name=self.name,
            fullAddress=str(self.country) + ', ' + str(self.city) + ', ' + str(self.adress),
            stars=self.stars
        )

    def get_hotel_response(self):
        return HotelResponse(
            hotelUid=self.hotel_uid,
            name=self.name,
            country=self.country,
            city=self.city,
            address=self.adress,
            stars=self.stars,
            price=self.price
        )
    
class Reservation(Base):
    __tablename__ = 'reservation'
    __table_args__ = {
        'extend_existing': True,
        # 'CheckConstraint': CheckConstraint(f'CHECK (status in {str(list(DISCOUNT_BY_STATUS.keys()))})')
    }

    id = Column(Integer, primary_key=True)
    reservation_uid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4, unique=True)
    username = Column(VARCHAR(80), nullable=False)
    payment_uid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4, unique=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id', ondelete='CASCADE'), nullable=False)
    status = Column(VARCHAR(20), nullable=False, default='PAID')
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    def get_dto_model(self, db: Session):

        hotel = db.query(Hotel).filter(Hotel.id == self.hotel_id).first()

        return ReservationResponse(
            reservationUid=self.reservation_uid,
            hotel=hotel.get_hotel_info(),
            startDate=self.start_date,
            endDate=self.end_date,
            status=self.status,
            paymentUid=self.payment_uid
        )
    
    def get_created_reservation(self, db: Session):

        hotel = db.query(Hotel).filter(Hotel.id == self.hotel_id).first()
        
        return CreateReservationResponse(
            reservationUid=self.reservation_uid,
            hotelUid=hotel.hotel_uid,
            startDate=self.start_date,
            endDate=self.end_date,
            status=self.status,
            paymentUid=self.payment_uid
        )
    
    def get_updated_reservation(self, db: Session):

        hotel = db.query(Hotel).filter(Hotel.id == self.hotel_id).first()
        
        return CreateReservationResponse(
            hotelUid=hotel.hotel_uid,
            startDate=self.start_date,
            endDate=self.end_date,
            status=self.status,
            paymentUid=self.payment_uid,
            reservationUid=self.reservation_uid
        )
    
    def update_reservation_status(self, new_reservation_status: str):
        self.status = new_reservation_status
