from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

from transporte.models import Route, Bus, Driver, Trip, Ticket


def create_user(username='user', email=None, password='Pass1234!', **kwargs):
    email = email or f'{username}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, **kwargs
    )


def create_staff(username='staff', email=None, password='Admin1234!'):
    email = email or f'{username}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, is_staff=True
    )


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def auth_client(user):
    client = APIClient()
    access, _ = get_tokens(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    return client


def create_route(name='Ruta Norte', origin='Quito', destination='Ibarra',
                 distance=120, base_price=8.50, duration=None, is_active=True):
    if duration is None:
        duration = timedelta(hours=3)
    return Route.objects.create(
        name=name, origin=origin, destination=destination,
        distance=distance, base_price=base_price,
        duration=duration, is_active=is_active,
    )


def create_bus(plate='PCC-1234', brand='Mercedes', model='Sprinter',
               year=2022, capacity=40, is_active=True):
    return Bus.objects.create(
        plate=plate, brand=brand, model=model,
        year=year, capacity=capacity, is_active=is_active,
    )


def create_driver(user=None, license_number='LIC-001', phone='0999999999', is_active=True):
    if user is None:
        user = create_user('driver1')
    return Driver.objects.create(
        user=user, license_number=license_number,
        phone=phone, is_active=is_active,
    )


def create_trip(bus=None, route=None, driver=None, status='scheduled', price=8.50):
    if bus is None:
        bus = create_bus()
    if route is None:
        route = create_route()
    if driver is None:
        driver = create_driver()
    now = datetime.now()
    departure = now + timedelta(hours=1)
    arrival = now + timedelta(hours=4)
    return Trip.objects.create(
        bus=bus, route=route, driver=driver,
        departure_time=departure, arrival_time=arrival,
        price=price, status=status,
    )


def create_ticket(trip=None, user=None, passenger_name='Juan Perez',
                  passenger_id='1234567890', seat_number=1):
    if trip is None:
        trip = create_trip()
    if user is None:
        user = create_user('passenger')
    return Ticket.objects.create(
        trip=trip, user=user,
        passenger_name=passenger_name,
        passenger_id=passenger_id,
        seat_number=seat_number,
        price=trip.price,
    )
