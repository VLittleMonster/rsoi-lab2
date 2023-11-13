from models import Payment
from sqlalchemy.orm import Session
from schemas.dto import PaymentInfo
from schemas.dto import PaymentUids
from fastapi import status
from fastapi.exceptions import HTTPException
from uuid import UUID

async def get_payments(data: list[PaymentUids], db: Session) -> list:
    payments = []

    for id in data:
        try:
            payment = db.query(Payment).filter(Payment.payment_uid == id.uid).first()
        except:
            return list()
        payments.append(payment.get_payment_info())
    
    return payments


async def create_payment(payment_price: int, db: Session) -> Payment:
    new_payment= Payment(payment_price=payment_price)
    try:
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
    except Exception as e:
        print(e)

    return new_payment


async def update_payment(paymentUid: UUID, data: PaymentInfo, db: Session) -> Payment:
    payment = db.query(Payment).filter(Payment.payment_uid == paymentUid).first()

    if payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if data.status:
        payment.update_payment_status(data.status)
    if data.price:
        payment.update_payment_price(data.price)
    
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment
