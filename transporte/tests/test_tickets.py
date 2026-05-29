from django.test import TestCase
from rest_framework import status

from .helpers import (
    create_user, create_staff, auth_client,
    create_trip, create_ticket,
)


class TicketCRUDTests(TestCase):

    def setUp(self):
        self.user   = create_user('laura')
        self.client = auth_client(self.user)
        self.trip   = create_trip()

    def test_create_ticket(self):
        resp = self.client.post('/api/tickets/', {
            'trip': self.trip.id,
            'passenger_name': 'Laura Maria',
            'passenger_id': '1234567890',
            'seat_number': 5,
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['passenger_name'], 'Laura Maria')
        self.assertIn('trip_info', resp.data)

    def test_list_own_tickets(self):
        create_ticket(trip=self.trip, user=self.user)
        resp = self.client.get('/api/tickets/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_cannot_book_taken_seat(self):
        create_ticket(trip=self.trip, user=self.user, seat_number=1)
        resp = self.client.post('/api/tickets/', {
            'trip': self.trip.id,
            'passenger_name': 'Other',
            'passenger_id': '999',
            'seat_number': 1,
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_book_non_scheduled_trip(self):
        self.trip.status = 'completed'
        self.trip.save()
        resp = self.client.post('/api/tickets/', {
            'trip': self.trip.id,
            'passenger_name': 'Test',
            'passenger_id': '111',
            'seat_number': 10,
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class TicketPermissionTests(TestCase):

    def setUp(self):
        self.user1  = create_user('mario')
        self.user2  = create_user('luigi')
        self.staff  = create_staff()
        self.trip   = create_trip()
        self.ticket = create_ticket(trip=self.trip, user=self.user1)

    def test_user_cannot_see_others_ticket(self):
        resp = auth_client(self.user2).get(f'/api/tickets/{self.ticket.id}/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_staff_can_see_any_ticket(self):
        resp = auth_client(self.staff).get(f'/api/tickets/{self.ticket.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_staff_can_cancel_ticket(self):
        resp = auth_client(self.staff).post(f'/api/tickets/{self.ticket.id}/cancel/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 'cancelled')

    def test_stats_staff_only(self):
        resp = auth_client(self.staff).get('/api/tickets/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total_tickets', 'total_revenue', 'by_status']:
            self.assertIn(field, resp.data)

    def test_stats_regular_user_returns_403(self):
        resp = auth_client(self.user1).get('/api/tickets/stats/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
