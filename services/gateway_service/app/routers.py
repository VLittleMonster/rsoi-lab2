from fastapi import APIRouter, status, Header
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from uuid import UUID

import services as GatewayService
import schemas.dto as schemas
from schemas.responses import ResponsesEnum
from config.config import get_settings

router = APIRouter(prefix='', tags=['Gateway API'])
settings = get_settings()


@router.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_availability():
    return Response(status_code=status.HTTP_200_OK)


@router.get(f'{settings["prefix"]}/hotels', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.PaginationResponse.value
            })
async def get_all_hotels(page: int = 0, size: int = 0):
    return await GatewayService.get_all_hotels(page, size)


@router.get(f'{settings["prefix"]}/me', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.UserInfoResponse.value
            })
async def get_user_info(username: str = Header(alias='X-User-Name')):
    return await GatewayService.get_user_info(username)


@router.get(f'{settings["prefix"]}/loyalty', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.LoyaltyInfoResponse.value
            })
async def get_loyalty(username: str = Header(alias='X-User-Name')):
    return await GatewayService.get_loyalty(username)


@router.get(f'{settings["prefix"]}/reservations', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationsResponse.value
            })
async def get_reservations(username: str = Header(alias='X-User-Name')):
    return await GatewayService.get_reservations(username)


@router.get(f'{settings["prefix"]}/reservations/' + '{reservationUid}', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationResponse.value,
                status.HTTP_404_NOT_FOUND: ResponsesEnum.ErrorResponse.value
            })
async def get_reservation_by_uid(reservationUid: UUID, username: str = Header(alias='X-User-Name')):
    reservation = await GatewayService.get_reservation_by_uid(reservationUid, username)
    if reservation is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=schemas.ErrorResponse().model_dump())
    return reservation


@router.post(f'{settings["prefix"]}/reservations', status_code=status.HTTP_200_OK,
             responses={
                 status.HTTP_200_OK: ResponsesEnum.CreateReservationResponse.value,
                 status.HTTP_400_BAD_REQUEST: ResponsesEnum.ValidationErrorResponse.value
             })
async def create_reservation(reservRequest: schemas.CreateReservationRequest,
                             username: str = Header(alias='X-User-Name')):
    try:
        reservation = await GatewayService.create_reservation(reservRequest, username)
    except RequestValidationError as exc:
        details = [schemas.ErrorDescription(
            field=e["field"],
            error=e["msg"]
        ) for e in jsonable_encoder(exc.errors())]

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=schemas.ValidationErrorResponse(
            message='Invalid request',
            errors=list(details)
        ).model_dump())
    return reservation


@router.delete(f'{settings["prefix"]}/reservations/' + '{reservationUid}', status_code=status.HTTP_204_NO_CONTENT,
               responses={
                   status.HTTP_404_NOT_FOUND: ResponsesEnum.ErrorResponse.value
               })
async def delete_reservation(reservationUid: UUID, username: str = Header(alias='X-User-Name')):
    resp = await GatewayService.delete_reservation(reservationUid, username)
    if resp is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=schemas.ErrorResponse().model_dump())
    return Response(status_code=status.HTTP_204_NO_CONTENT)
