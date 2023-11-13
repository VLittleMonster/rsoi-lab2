from fastapi import APIRouter, Depends, status, Header, Response, Request
from sqlalchemy.orm import Session
from database.AppDatabase import AppDatabase
from config.config import get_settings

import services as LoyaltyService
from schemas.responses import ResponsesEnum
from schemas.dto import LoyaltyInfoRequest

router = APIRouter(prefix='', tags=['Loyalty REST API operations'])
app_db = AppDatabase.app_db
settings = get_settings()


@router.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_availability():
    return Response(status_code=status.HTTP_200_OK)


@router.get(f'{settings["prefix"]}/', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.LoyaltyInfoResponse.value
            })
async def get_loyalty(username: str = Header(alias='X-User-Name'), db: Session = Depends(app_db.get_db)):
    loyalty = await LoyaltyService.get_loyalty(username, db)
    return ResponsesEnum.get_loyalty_response(loyalty)


@router.patch(f'{settings["prefix"]}/', status_code=status.HTTP_200_OK,
              responses={
                  status.HTTP_200_OK: ResponsesEnum.LoyaltyUpdateResponse.value
              })
async def update_loyalty(data: LoyaltyInfoRequest, username: str = Header(alias='X-User-Name'), db: Session = Depends(app_db.get_db)):
    await LoyaltyService.update_loyalty(data, username, db)
    return Response(status_code=status.HTTP_200_OK)
