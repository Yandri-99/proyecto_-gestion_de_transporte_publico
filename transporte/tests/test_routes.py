from django.test import TestCase
from rest_framework import status

from .helpers import create_user, create_staff, auth_client, create_route


class RoutePermissionTests(TestCase):

    def setUp(self):
        self.user   = create_user('eve')
        self.staff  = create_staff()
        self.route  = create_route()

    def test_authenticated_user_can_list(self):
        resp = auth_client(self.user).get('/api/routes/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthenticated_returns_401(self):
        from rest_framework.test import APIClient
        resp = APIClient().get('/api/routes/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_cannot_create(self):
        resp = auth_client(self.user).post('/api/routes/', {
            'name': 'Test', 'origin': 'A', 'destination': 'B',
            'distance': 50, 'base_price': '5.00',
            'duration': '02:00:00',
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_create(self):
        resp = auth_client(self.staff).post('/api/routes/', {
            'name': 'Ruta Sur', 'origin': 'Quito', 'destination': 'Latacunga',
            'distance': 85, 'base_price': '5.50',
            'duration': '01:30:00', 'is_active': True,
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_staff_can_delete(self):
        resp = auth_client(self.staff).delete(f'/api/routes/{self.route.id}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)


class RouteFilterTests(TestCase):

    def setUp(self):
        self.client = auth_client(create_user('filters'))
        create_route('Ruta Norte', origin='Quito', destination='Ibarra', is_active=True)
        create_route('Ruta Sur', origin='Quito', destination='Latacunga', is_active=False)

    def test_filter_by_active(self):
        resp = self.client.get('/api/routes/?is_active=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['results'][0]['name'], 'Ruta Norte')

    def test_search_by_name(self):
        resp = self.client.get('/api/routes/?search=Ruta')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 2)

    def test_stats_returns_expected_fields(self):
        resp = self.client.get('/api/routes/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total', 'active', 'inactive', 'detail']:
            self.assertIn(field, resp.data)
