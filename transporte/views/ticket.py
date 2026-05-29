from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum

from transporte.models import Ticket, Trip
from transporte.serializers.ticket import TicketSerializer
from transporte.permissions import IsStaffOrReadOnly
from transporte.filters    import TicketFilter
from transporte.pagination import StandardPagination


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class   = TicketSerializer
    permission_classes = [IsAuthenticated]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = TicketFilter
    search_fields      = ['passenger_name', 'passenger_id']
    ordering_fields    = ['created_at', 'seat_number']
    ordering           = ['-created_at']
    http_method_names  = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        if self.request.user.is_staff:
            return (
                Ticket.objects
                .select_related('trip__route', 'trip__bus', 'user')
                .all()
            )
        return (
            Ticket.objects
            .filter(user=self.request.user)
            .select_related('trip__route', 'trip__bus')
        )

    def perform_create(self, serializer):
        trip = serializer.validated_data['trip']
        serializer.save(
            user=self.request.user,
            price=trip.price,
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser], url_path='cancel')
    def cancel(self, request, pk=None):
        ticket = self.get_object()
        if ticket.status != 'confirmed':
            return Response(
                {'error': f'Ticket already {ticket.status}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ticket.status = 'cancelled'
        ticket.save(update_fields=['status'])
        return Response(TicketSerializer(ticket).data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser], url_path='stats')
    def stats(self, request):
        qs = Ticket.objects.all()
        totals = qs.aggregate(
            total_tickets = Count('id'),
            total_revenue = Sum('price'),
        )
        by_status = {
            s: qs.filter(status=s).count()
            for s, _ in Ticket.STATUS_CHOICES
        }
        return Response({
            'total_tickets': totals['total_tickets'],
            'total_revenue': float(totals['total_revenue'] or 0),
            'by_status':     by_status,
        })
