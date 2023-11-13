from copy import deepcopy
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
import asyncio

from unit_tests.mock_data import LoyaltiesMock
from database.database import Database
from schemas.dto import LoyaltyInfoRequest, LoyaltyInfoResponse
from models import Loyalty, DISCOUNT_BY_STATUS

import services as LoyaltyService

loyalties = deepcopy(LoyaltiesMock.mocks)
test_database = Database("sqlite:///test_loyalties.db")
test_database.create_all()
test_db = next(test_database.get_db())


def check_equality(a: LoyaltyInfoResponse, b: dict):
    return (a.status == b['status'] and
            a.discount == b['discount'] and
            a.reservationCount == b['reservationCount'])


def init_db(db: Session, init_data: list):
    for data in init_data:
        loyalty = asyncio.run(LoyaltyService.create_loyalty(data['username'], db))
        assert loyalty.username == data['username'], 'Initial error: ' + loyalty.username + " != " + data['username']
        loyalty_dto = loyalty.get_dto_model()
        data['reservationCount'] = loyalty_dto.reservationCount
        data['status'] = loyalty_dto.status
        data['discount'] = loyalty_dto.discount


init_db(test_db, loyalties)


async def test_get_by_username_success():
    try:
        for loyalty in loyalties:
            received_loyalty = (await LoyaltyService.get_loyalty(loyalty['username'], test_db)).get_dto_model()

            assert received_loyalty is None or check_equality(received_loyalty, loyalty), \
                f'Error in getting loyalty: equality error: {received_loyalty} and {loyalty}'

        received_loyalty = (await LoyaltyService.get_loyalty('username', test_db)).get_dto_model()
        loyalty = {
            'username:': 'username',
            'reservationCount': 0,
            'status': 'BRONZE',
            'discount': 5
        }
        assert received_loyalty is None or check_equality(received_loyalty, loyalty), \
                f'Error in getting loyalty: equality error: {received_loyalty} and {loyalty}'

    except Exception as e:
        assert False, 'Exception in getting loyalty: ' + str(e)


async def test_update_by_username_success():
    try:
        for i in range(1, 25):
            update_data = LoyaltyInfoRequest(
                reservationCountOperation=1
            )
            loyalty = (await LoyaltyService.update_loyalty(update_data, loyalties[0]['username'], test_db)).get_dto_model()
            correct_loyalty = {
                'reservationCount': i,
                'status': Loyalty.get_status_by_reservation_count(i),
                'discount': DISCOUNT_BY_STATUS[Loyalty.get_status_by_reservation_count(i)]
            }

            assert check_equality(loyalty, correct_loyalty), \
                f'Error in updating loyalty (success): {loyalty} is not equal {correct_loyalty}'
    except Exception as e:
        assert False, 'Exception in updating person: ' + str(e)


async def test_update_by_username_not_found():
    try:
        update_data = LoyaltyInfoRequest(
                reservationCountOperation=10
        )
        await LoyaltyService.update_loyalty(update_data, 'unknown_name', test_db)
        assert False, 'in updating person (not found): no 404 exception'
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            assert True
        else:
            assert False, 'HttpException in updating person: is not 404 exception ' + str(e)
    except Exception as e:
        assert False, 'Exception in updating person: is not 404 exception ' + str(e)
