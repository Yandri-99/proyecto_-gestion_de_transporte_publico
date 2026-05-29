from django.test import TestCase
from rest_framework import status

from .helpers import (
    create_user, create_staff, auth_client,
    create_route, create_bus, create_driver, create_trip,
)


class TripCRUDTests(TestCase):

    def setUp(self):
        self.staff  = create_staff()
        self.client = auth_client(self.staff)
        self.route  = create_route()
        self.bus    = create_bus()
        self.driver = create_driver()
        self.trip   = create_trip(bus=self.bus, route=self.route, driver=self.driver)

    def test_create_trip(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        resp = self.client.post('/api/trips/', {
            'route': self.route.id,
            'bus': self.bus.id,
            'driver': self.driver.id,
            'departure_time': (now + timedelta(days=1)).isoformat(),
            'arrival_time': (now + timedelta(days=1, hours=3)).isoformat(),
            'price': '10.00',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['status'], 'scheduled')

    def test_list_trips(self):
        resp = self.client.get('/api/trips/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('results', resp.data)

    def test_start_trip(self):
        resp = self.client.post(f'/api/trips/{self.trip.id}/start/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 'in_progress')

    def test_complete_trip(self):
        self.trip.status = 'in_progress'
        self.trip.save()
        resp = self.client.post(f'/api/trips/{self.trip.id}/complete/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 'completed')

    def test_cancel_trip(self):
        resp = self.client.post(f'/api/trips/{self.trip.id}/cancel/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 'cancelled')

    def test_cannot_start_completed_trip(self):
        self.trip.status = 'completed'
        self.trip.save()
        resp = self.client.post(f'/api/trips/{self.trip.id}/start/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class TripPermissionTests(TestCase):

    def setUp(self):
        self.user  = create_user('ivan')
        self.staff = create_staff()
        self.trip  = create_trip()

    def test_regular_user_can_view_scheduled(self):
        resp = auth_client(self.user).get(f'/api/trips/{self.trip.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_start_trip(self):
        resp = auth_client(self.user).post(f'/api/trips/{self.trip.id}/start/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_schedule_endpoint(self):
        resp = auth_client(self.user).get('/api/trips/schedule/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_stats_staff_only(self):
        resp = auth_client(self.staff).get('/api/trips/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total_trips', 'total_revenue', 'by_status']:
            self.assertIn(field, resp.data)
