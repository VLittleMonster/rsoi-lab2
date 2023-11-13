from fastapi import status
from fastapi.exceptions import RequestValidationError
from config.config import get_settings
from typing import Final
from schemas import dto as schemas
import serviceRequests
from uuid import UUID

username_in_header: Final = 'X-User-Name'
settings = get_settings()


async def get_all_hotels(page: int, size: int):
    url = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}{settings['prefix']}" \
          f"/hotels?page={page}&size={size}"
    resp = serviceRequests.get(url)
    if resp is None or resp.status_code != status.HTTP_200_OK:
        return []
    return resp.json()


async def get_user_info(username: str):
    loyalty_response = await get_loyalty(username)
    reservation_response = await get_reservations(username)
    return schemas.UserInfoResponse(reservations=reservation_response, loyalty=loyalty_response)


async def get_reservations(username: str):
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}" \
                      f"{settings['prefix']}/reservations"
    url_payment_serv = f"http://{settings['payment_serv_host']}:{settings['payment_serv_port']}{settings['prefix']}" \
                       f"/payments"
    resp = serviceRequests.get(url_reserv_serv, headers={'X-User-Name': username})
    if resp is None or resp.status_code != status.HTTP_200_OK:
        return []

    reservation_responses = resp.json()
    pay_uuids = []
    for res in reservation_responses:
        pay_uuids.append({'uid': res['paymentUid']})
    print(pay_uuids)
    resp = serviceRequests.patch(url_payment_serv, data=pay_uuids)
    print(resp)

    if resp is None or resp.status_code != status.HTTP_200_OK:
        return []

    payment_responses = resp.json()

    res = []
    for i in range(len(reservation_responses)):
        res.append(schemas.ReservationResponse(
            reservationUid=reservation_responses[i]['reservationUid'],
            hotel=reservation_responses[i]['hotel'],
            startDate=reservation_responses[i]['startDate'],
            endDate=reservation_responses[i]['endDate'],
            status=reservation_responses[i]['status'],
            payment=schemas.PaymentInfo(
                status=payment_responses[i]['status'],
                price=payment_responses[i]['price']
            )
        ))
    return res


async def get_reservation_by_uid(reservaionUid: UUID, username: str):
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}" \
                      f"{settings['prefix']}/reservations/{reservaionUid}"
    url_payment_serv = f"http://{settings['payment_serv_host']}:{settings['payment_serv_port']}{settings['prefix']}" \
                       f"/payments"
    reservation_response = serviceRequests.get(url_reserv_serv, headers={'X-User-Name': username})
    if reservation_response is None or reservation_response.status_code != status.HTTP_200_OK:
        return None

    reservation_response = reservation_response.json()
    resp = serviceRequests.patch(url_payment_serv, data=[{"uid": reservation_response["paymentUid"]}])

    if resp is None or resp.status_code != status.HTTP_200_OK:
        print(resp)
        return None

    payment_response = resp.json()

    return schemas.ReservationResponse(
            reservationUid=reservation_response['reservationUid'],
            hotel=reservation_response['hotel'],
            startDate=reservation_response['startDate'],
            endDate=reservation_response['endDate'],
            status=reservation_response['status'],
            payment=schemas.PaymentInfo(
                status=payment_response[0]['status'],
                price=payment_response[0]['price']
            )
           )


async def create_reservation(reservRequest: schemas.CreateReservationRequest, username: str):
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}{settings['prefix']}"
    url_payment_serv = f"http://{settings['payment_serv_host']}:{settings['payment_serv_port']}{settings['prefix']}"
    url_loyalty_serv = f"http://{settings['loyalty_serv_host']}:{settings['loyalty_serv_port']}{settings['prefix']}" \
                       f"/loyalty"
    header = {"X-User-Name": username}
    resp = serviceRequests.get(url_reserv_serv + f'/hotels/{reservRequest.hotelUid}')

    if resp is None or resp.status_code != status.HTTP_200_OK:
        raise RequestValidationError(errors=[{"field": "hotelUid",
                                              "msg": "invalid hotel uuid. no such hotel"}])

    hotel_resp = resp.json()
    cost = (reservRequest.endDate - reservRequest.startDate).days*hotel_resp['price']
    loyalty_info: schemas.LoyaltyInfoResponse = (await get_loyalty(username))

    if loyalty_info is None:
        raise RequestValidationError(errors=[{"field": "username",
                                              "msg": "client with such username does not exist"}])

    cost *= 0.01*(100-loyalty_info['discount'])
    cost = int(cost + 0.5)
    resp = serviceRequests.post(url_payment_serv + f'/payments', headers={"X-Payment-Price": str(int(cost))})

    if resp is None or resp.status_code != status.HTTP_200_OK:
        print(cost)
        print(resp)
        raise RequestValidationError(errors=[{"field": "payment_info",
                                              "msg": "error in POST payment"}])

    pay_info = resp.json()
    resp = serviceRequests.patch(url_loyalty_serv, headers=header, data=schemas.LoyaltyInfoRequest(
        reservationCountOperation=1
    ).model_dump(mode='json'))

    if resp is None or resp.status_code != status.HTTP_200_OK:
        raise RequestValidationError(errors=[{"field": "loyalty",
                                              "msg": "error in PATCH method"}])

    resp = serviceRequests.post(url_reserv_serv + f'/reservations', headers=header,
                                data=schemas.CreateReservationRequestForReservService(
                                    paymentUid=pay_info['uid'],
                                    hotelUid=hotel_resp['hotelUid'],
                                    startDate=reservRequest.startDate,
                                    endDate=reservRequest.endDate
                                ).model_dump(mode='json'))

    if resp is None or resp.status_code != status.HTTP_200_OK:
        print(schemas.CreateReservationRequestForReservService(
                                    paymentUid=pay_info['uid'],
                                    hotelUid=hotel_resp['hotelUid'],
                                    startDate=reservRequest.startDate,
                                    endDate=reservRequest.endDate
                                ).model_dump(mode='json'))
        print(resp)
        raise RequestValidationError(errors=[{"field": "reservation",
                                              "msg": "error in POST reservation method"}])

    reservResponse = resp.json()
    return schemas.CreateReservationResponse(
        reservationUid=reservResponse['reservationUid'],
        hotelUid=reservResponse['hotelUid'],
        startDate=reservResponse['startDate'],
        endDate=reservResponse['endDate'],
        discount=loyalty_info['discount'],
        status=reservResponse['status'],
        payment=schemas.PaymentInfo(
                status=pay_info['status'],
                price=pay_info['price']
        )
    )


async def delete_reservation(reservationUid: UUID, username: str):
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}{settings['prefix']}"
    url_payment_serv = f"http://{settings['payment_serv_host']}:{settings['payment_serv_port']}{settings['prefix']}"
    url_loyalty_serv = f"http://{settings['loyalty_serv_host']}:{settings['loyalty_serv_port']}{settings['prefix']}" \
                       f"/loyalty"
    header = {"X-User-Name": username}
    resp = serviceRequests.patch(url_reserv_serv + f'/reservations/{reservationUid}', headers=header,
                                 data=schemas.UpdateReservationRequestForReservService(
                                     status='CANCELED'
                                 ).model_dump(mode='json'))

    if resp is None or resp.status_code != status.HTTP_200_OK:
        print("error in PATCH reservation method")
        print("headers:", header)
        print(schemas.UpdateReservationRequestForReservService(status='CANCELED').model_dump(mode='json'))
        print(resp)
        return None

    reserv_info_resp = resp.json()
    resp = serviceRequests.patch(url_payment_serv + f'/payments/{reserv_info_resp["paymentUid"]}',
                                 data=schemas.UpdatePaymentRequest(
                                     status='CANCELED'
                                 ).model_dump(mode='json'))

    if resp is None or resp.status_code != status.HTTP_200_OK:
        print("error in PATCH payment method")
        print(schemas.UpdatePaymentRequest(status='CANCELED').model_dump(mode='json'))
        print(resp)
        return None

    resp = serviceRequests.patch(url_loyalty_serv, headers=header, data=schemas.LoyaltyInfoRequest(
        reservationCountOperation=-1
    ).model_dump(mode='json'))

    if resp is None or resp.status_code != status.HTTP_200_OK:
        print("error in PATCH loyalty method")
        print("headers:", header)
        print(schemas.LoyaltyInfoRequest(reservationCountOperation=-1).model_dump(mode='json'))
        print(resp)
        return None

    return status.HTTP_204_NO_CONTENT


async def get_loyalty(username: str):
    url_loyalty_serv = f"http://{settings['loyalty_serv_host']}:{settings['loyalty_serv_port']}{settings['prefix']}" \
                       f"/loyalty"
    response = serviceRequests.get(url_loyalty_serv, headers={'X-User-Name': username})

    if response is None or response.status_code != status.HTTP_200_OK:
        print("error in GET loyalty method")
        print("headers:", {'X-User-Name': username})
        print(response)
        return None
    return response.json()
