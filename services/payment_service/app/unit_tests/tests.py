from copy import deepcopy
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from uuid import UUID
import asyncio

from unit_tests.mock_data import PaymentsMock
from database.database import Database
from schemas.dto import PaymentInfo
from schemas.dto import PaymentUids

import services as PaymentService

payments = deepcopy(PaymentsMock.mocks)
uids = []
test_database = Database("sqlite:///test_payment.db")
test_database.create_all()
test_db = next(test_database.get_db())


def check_equality(a: PaymentInfo, b: dict):
    return (a['status'] == b['status'] and
            a['price'] == b['price'] and
            a['uid'] == b['uid'])


async def init_db(db: Session, init_data: list):
    for data in init_data:
        payment = asyncio.run(PaymentService.create_payment(data['price'], db))
        assert payment.price == data['price'], 'Initial error: ' + payment.price + " != " + data['price']
        payment_dto = payment.get_dto_model()
        data['price'] = payment_dto.price
        data['status'] = payment_dto.status
        data['uid'] = payment_dto.uid
        uids.append(payment_dto.uid)


init_db(test_db, payments)


async def test_get_payments():
    try:
        paymentUids = [PaymentUids(uid=uids[0]), PaymentUids(uid=uids[1]), PaymentUids(uid=uids[2])]
        received_payments = await PaymentService.get_payments(paymentUids, test_db)

        for i in range(len(received_payments)):
            assert received_payments[i] is None or check_equality(received_payments[i], payments[i]), \
                f'Error in getting payments: equality error: {received_payments[i]} and {payments[i]}'

    except Exception as e:
        assert False, 'Exception in getting payments: ' + str(e)


async def test_update_by_uid_success():
    try:
        for uid in uids:
            update_data = PaymentInfo(
                price=666, status='PAID'
            )
            payment = (await PaymentService.update_payment(uid, update_data, test_db)).get_dto_model()
            correct_payment = {
                'price': 666,
                'status': 'PAID',
                'uid': uid
            }
            assert check_equality(payment, correct_payment), \
                f'Error in updating payment (success): {payment} is not equal {correct_payment}'
    except Exception as e:
        assert False, 'Exception in updating payment: ' + str(e)


async def test_update_by_uid_not_found():
    try:
        update_data = PaymentInfo(
            price=666, status='PAID'
        )
        await PaymentService.update_payment(UUID('12345678123456781234567812345678'), update_data, test_db)
        assert False, 'in updating payment (not found): no 404 exception'
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            assert True
        else:
            assert False, 'HttpException in updating payment: is not 404 exception ' + str(e)
    except Exception as e:
        assert False, 'Exception in updating payment: is not 404 exception ' + str(e)
