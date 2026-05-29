from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .helpers import create_user, create_staff, auth_client, create_bus


class BusPermissionTests(TestCase):

    def setUp(self):
        self.user  = create_user('frank')
        self.staff = create_staff()
        self.bus   = create_bus()

    def test_authenticated_can_list(self):
        resp = auth_client(self.user).get('/api/buses/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('results', resp.data)

    def test_unauthenticated_returns_401(self):
        resp = APIClient().get('/api/buses/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_cannot_create(self):
        resp = auth_client(self.user).post('/api/buses/', {
            'plate': 'XYZ-999', 'brand': 'Toyota', 'model': 'Coaster',
            'year': 2023, 'capacity': 30,
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_create(self):
        resp = auth_client(self.staff).post('/api/buses/', {
            'plate': 'ABC-123', 'brand': 'Mercedes', 'model': 'Sprinter',
            'year': 2024, 'capacity': 40,
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_duplicate_plate_returns_400(self):
        create_bus(plate='DUPE-01')
        resp = auth_client(self.staff).post('/api/buses/', {
            'plate': 'dupe-01', 'brand': 'Test', 'model': 'Test',
            'year': 2020, 'capacity': 20,
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class BusFilterTests(TestCase):

    def setUp(self):
        self.client = auth_client(create_user('gina'))
        create_bus(plate='AAA-001', brand='Mercedes', capacity=40)
        create_bus(plate='BBB-002', brand='Toyota', capacity=20)

    def test_filter_by_brand(self):
        resp = self.client.get('/api/buses/?brand=Mercedes')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_min_capacity(self):
        resp = self.client.get('/api/buses/?capacity_min=30')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        names = [b['plate'] for b in resp.data['results']]
        self.assertIn('AAA-001', names)
        self.assertNotIn('BBB-002', names)

    def test_search_by_plate(self):
        resp = self.client.get('/api/buses/?search=AAA')
        self.assertEqual(resp.data['count'], 1)

    def test_stats_returns_expected_fields(self):
        resp = self.client.get('/api/buses/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total', 'active', 'inactive', 'total_capacity']:
            self.assertIn(field, resp.data)
