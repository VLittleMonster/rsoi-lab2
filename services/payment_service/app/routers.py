from fastapi import APIRouter, Depends, status, Header, Response, Request
from sqlalchemy.orm import Session
from database.AppDatabase import AppDatabase
from config.config import get_settings

import services as PaymentService
from schemas.responses import ResponsesEnum
from schemas.dto import PaymentInfo
from schemas.dto import PaymentUids
from uuid import UUID

router = APIRouter(prefix='', tags=['Payment REST API operations'])
app_db = AppDatabase.app_db
settings = get_settings()


@router.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_availability():
    return Response(status_code=status.HTTP_200_OK)


@router.patch(f'{settings["prefix"]}', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.PaymentInfo.value
            })
async def get_payments(data: list[PaymentUids] = None, db: Session = Depends(app_db.get_db)):
    payments = await PaymentService.get_payments(data, db)
    return payments


@router.post(f'{settings["prefix"]}', status_code=status.HTTP_200_OK,
            responses={
                 status.HTTP_200_OK: ResponsesEnum.PaymentInfo.value
            })
async def create_payment(payment_price: int = Header(alias='X-Payment-Price'), db: Session = Depends(app_db.get_db)):
    payment = await PaymentService.create_payment(payment_price, db)
    return ResponsesEnum.get_payment_response(payment)


@router.patch(f'{settings["prefix"]}/' + '{paymentUid}', status_code=status.HTTP_200_OK,
              responses={
                  status.HTTP_200_OK: ResponsesEnum.PaymentUpdateResponse.value
              })
async def update_payment(paymentUid: UUID, data: PaymentInfo = None, db: Session = Depends(app_db.get_db)):
    payment = await PaymentService.update_payment(paymentUid, data, db)
    return ResponsesEnum.get_payment_response(payment)
