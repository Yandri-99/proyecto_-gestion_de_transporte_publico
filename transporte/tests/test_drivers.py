from django.test import TestCase
from rest_framework import status

from .helpers import create_user, create_staff, auth_client, create_driver


class DriverPermissionTests(TestCase):

    def setUp(self):
        self.user    = create_user('henry')
        self.staff   = create_staff()
        self.driver  = create_driver()

    def test_authenticated_can_list(self):
        resp = auth_client(self.user).get('/api/drivers/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthenticated_returns_401(self):
        from rest_framework.test import APIClient
        resp = APIClient().get('/api/drivers/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_cannot_create(self):
        driver_user = create_user('newdriver')
        resp = auth_client(self.user).post('/api/drivers/', {
            'user': driver_user.id,
            'license_number': 'LIC-999',
            'phone': '0999999999',
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_create(self):
        driver_user = create_user('driverstaff')
        resp = auth_client(self.staff).post('/api/drivers/', {
            'user': driver_user.id,
            'license_number': 'LIC-STAFF-01',
            'phone': '0998888888',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_duplicate_license_returns_400(self):
        driver_user = create_user('another')
        resp = auth_client(self.staff).post('/api/drivers/', {
            'user': driver_user.id,
            'license_number': 'LIC-001',
            'phone': '0997777777',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class DriverStatsTests(TestCase):

    def setUp(self):
        self.client = auth_client(create_staff())

    def test_stats_returns_expected_fields(self):
        resp = self.client.get('/api/drivers/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total', 'active', 'inactive']:
            self.assertIn(field, resp.data)
