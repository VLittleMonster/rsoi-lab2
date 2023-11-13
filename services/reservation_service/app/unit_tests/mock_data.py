from uuid import UUID
from datetime import datetime

class ReservationsMock:
    mocks = [
        {
            'username': 'Alex',
            'paymentUid': UUID('12345678123456781234567812345670'),
            'hotelUid': UUID('12345678123456781234567812345670'),
            'startDate': datetime.strptime('2023-01-01',"%Y-%m-%d").date(),
            'endDate': datetime.strptime('2023-01-04',"%Y-%m-%d").date()
        },
        {
            'username': 'Mike',
            'paymentUid': UUID('12345678123456781234567812345671'),
            'hotelUid': UUID('12345678123456781234567812345671'),
            'startDate': datetime.strptime('2023-01-01',"%Y-%m-%d").date(),
            'endDate': datetime.strptime('2023-01-23',"%Y-%m-%d").date()
        },
        {
            'username': 'John',
            'paymentUid': UUID('12345678123456781234567812345672'),
            'hotelUid': UUID('12345678123456781234567812345672'),
            'startDate': datetime.strptime('2023-01-01',"%Y-%m-%d").date(),
            'endDate': datetime.strptime('2023-01-24',"%Y-%m-%d").date()
        },
        {
            'username': 'Ivan',
            'paymentUid': UUID('12345678123456781234567812345673'),
            'hotelUid': UUID('12345678123456781234567812345670'),
            'startDate': datetime.strptime('2023-01-01',"%Y-%m-%d").date(),
            'endDate': datetime.strptime('2023-01-17',"%Y-%m-%d").date()
        },
        {
            'username': 'Anna',
            'paymentUid': UUID('12345678123456781234567812345674'),
            'hotelUid': UUID('12345678123456781234567812345672'),
            'startDate': datetime.strptime('2023-01-01',"%Y-%m-%d").date(),
            'endDate': datetime.strptime('2023-01-10',"%Y-%m-%d").date()
        },
        {
            'username': 'Helen',
            'paymentUid': UUID('12345678123456781234567812345675'),
            'hotelUid': UUID('12345678123456781234567812345672'),
            'startDate': datetime.strptime('2023-01-01',"%Y-%m-%d").date(),
            'endDate': datetime.strptime('2023-01-02',"%Y-%m-%d").date()
        }
    ]

    hotels = [
        {
            'id': 1,
            'hotel_uid': UUID('12345678123456781234567812345670'),
            'name': 'Dolphin Botanic Ultra Beach Resort',
            'country': 'Turkey',
            'city': 'Alanya',
            'adress': 'Chulpan Hamatova, 64',
            'stars': 5,
            'price': 30000
        },
        {
            'id': 2,
            'hotel_uid': UUID('12345678123456781234567812345671'),
            'name': 'Lady Gaga Beach Resort',
            'country': 'USA',
            'city': 'Los Angeles',
            'adress': 'Hot Avenue, 69',
            'stars': 4,
            'price': 300
        },
        {
            'id': 3,
            'hotel_uid': UUID('12345678123456781234567812345672'),
            'name': 'Jomtien Garden Hotel & Resort',
            'country': 'Thailand',
            'city': 'Pattaya',
            'adress': 'Chon Buri, 27',
            'stars': 3,
            'price': 1500
        }
    ]