from copy import deepcopy
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
import asyncio

from unit_tests.mock_data import ReservationsMock
from database.database import Database
from schemas.dto import HotelResponse, ReservationResponse, UpdateReservation
from models import Hotel

import services as ReservationService

reservations = deepcopy(ReservationsMock.mocks)
hotels = deepcopy(ReservationsMock.hotels)
uids = []
test_database = Database("sqlite:///test_reservations.db")
test_database.create_all()
test_db = next(test_database.get_db())


def check_hotel_equality(a: HotelResponse, b: dict):
    return (a['hotelUid'] == b['hotelUid'] and
            a['name'] == b['name'] and
            a['country'] == b['country'] and
            a['city'] == b['city'] and
            a['address'] == b['address'] and
            a['stars'] == b['stars'] and
            a['price'] == b['price'])


def check_reservation_equality(a: ReservationResponse, b: dict):
    return (a['reservationUid'] == b['reservationUid'] and
            a['hotelUid'] == b['hotelUid'] and
            a['startDate'] == b['startDate'] and
            a['endDate'] == b['endDate'] and
            a['status'] == b['status'] and
            a['paymentUid'] == b['paymentUid'])


async def init_db(db: Session, init_data1: list, init_data2: list):
    for hotel in init_data1:
        new_hotel = Hotel(
            id = hotel['id'],
            hotel_uid = hotel['hotel_uid'],
            name = hotel['name'],
            country = hotel['country'],
            city = hotel['city'],
            adress = hotel['adress'],
            stars = hotel['stars'],
            price = hotel['price']
        )

        db.add(new_hotel)
        db.commit()
        db.refresh(new_hotel)

    for data in init_data2:
        reservation = asyncio.run(ReservationService.create_reservation(data['username'], data, db))
        assert reservation.paymentUid == data['paymentUid'], 'Initial error: ' + reservation.paymentUid + " != " + data['paymentUid']
        assert reservation.hotelUid == data['hotelUid'], 'Initial error: ' + reservation.hotelUid + " != " + data['hotelUid']
        assert reservation.startDate == data['startDate'], 'Initial error: ' + reservation.startDate + " != " + data['startDate']
        assert reservation.endDate == data['endDate'], 'Initial error: ' + reservation.endDate + " != " + data['endDate']
        reservation_dto = reservation.get_created_reservation()
        data['status'] = reservation_dto.status
        data['reservationUid'] = reservation_dto.reservationUid
        uids.append(data['reservationUid'])


init_db(test_db, hotels, reservations)


async def test_get_hotel_success():
    try:
        received_hotel = await ReservationService.get_hotel(UUID('12345678123456781234567812345671'), test_db)

        hotel = {
            'id': 2,
            'hotel_uid': UUID('12345678123456781234567812345671'),
            'name': 'Lady Gaga Beach Resort',
            'country': 'USA',
            'city': 'Los Angeles',
            'adress': 'Hot Avenue, 69',
            'stars': 4,
            'price': 300
        }

        assert received_hotel is None or check_reservation_equality(received_hotel, hotel), \
            f'Error in getting hotel: equality error: {received_hotel} and {hotel}'

    except Exception as e:
        assert False, 'Exception in getting hotel: ' + str(e)


async def test_get_hotel_not_found():
    try:
        await ReservationService.get_hotel(UUID('12345678123456781234567812345678'), test_db)
        assert False, 'in getting reservation (not found): no 404 exception'
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            assert True
        else:
            assert False, 'HttpException in getting reservation: is not 404 exception ' + str(e)
    except Exception as e:
        assert False, 'Exception in getting reservation: is not 404 exception ' + str(e)


async def test_get_reservation_success():
    try:
        received_reservation = await ReservationService.get_reservation(uids[0], 'Alex', test_db)

        """reservation = {
            'reservationUid': uids[0],
            'hotelUid': UUID('12345678123456781234567812345670'),
            'startDate': datetime.strptime('2023-01-01',"%Y-%m-%d").date(),
            'endDate': datetime.strptime('2023-01-04',"%Y-%m-%d").date(),
            'status': 'PAID',
            'paymentUid': UUID('12345678123456781234567812345670')
        }"""

        assert received_reservation is None or check_reservation_equality(received_reservation, reservations[0]), \
            f'Error in getting reservation: equality error: {received_reservation} and {reservations[0]}'

    except Exception as e:
        assert False, 'Exception in getting reservation: ' + str(e)


async def test_get_reservations_success():
    try:
        received_reservations = await ReservationService.get_reservations('Alex', test_db)

        alex_reservs = {}
        for reservation in reservations:
            if reservation['username'] == 'Alex':
                alex_reservs[str(reservation['reservationUid'])] = reservation

        for i in range(len(received_reservations)):
            assert received_reservations[i] is None or \
                   check_reservation_equality(received_reservations[i], alex_reservs[str(received_reservations[i]['reservationUid'])]), \
                f'Error in getting reservations: equality error: {received_reservations[i]} and {reservations[i]}'

    except Exception as e:
        assert False, 'Exception in getting reservations: ' + str(e)


async def test_get_reservation_not_found():
    try:
        await ReservationService.get_reservation(UUID('12345678123456781234567812345670'), 'LadyGaga', test_db)
        assert False, 'in getting reservation (not found): no 404 exception'
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            assert True
        else:
            assert False, 'HttpException in getting reservation: is not 404 exception ' + str(e)
    except Exception as e:
        assert False, 'Exception in getting reservation: is not 404 exception ' + str(e)


async def test_update_reservation_success():
    try:
        update_data = UpdateReservation(
            status='CANCELED'
        )
        reservation = await ReservationService.update_reservation(UUID('12345678123456781234567812345671'), update_data, 'Mike', test_db)
        correct_reservation = {
            'reservationUid': uids[1],
            'paymentUid': UUID('12345678123456781234567812345670'),
            'hotelUid': UUID('12345678123456781234567812345670'),
            'startDate': datetime.strptime('2023-01-01',"%Y-%m-%d").date(),
            'endDate': datetime.strptime('2023-01-04',"%Y-%m-%d").date(),
            'status': 'CANCELED'
        }

        assert check_reservation_equality(reservation, correct_reservation), \
            f'Error in updating reservation (success): {reservation} is not equal {correct_reservation}'
    except Exception as e:
        assert False, 'Exception in updating reservation: ' + str(e)


async def test_update_reservation_not_found():
    try:
        update_data = UpdateReservation(
            status='CANCELED'
        )
        await ReservationService.update_reservation(UUID('12345678123456781234567812345678'), update_data, 'Alex', test_db)
        assert False, 'in updating reservation (not found): no 404 exception'
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            assert True
        else:
            assert False, 'HttpException in updating reservation: is not 404 exception ' + str(e)
    except Exception as e:
        assert False, 'Exception in updating reservation: is not 404 exception ' + str(e)
