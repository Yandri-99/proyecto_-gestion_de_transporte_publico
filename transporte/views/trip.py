from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum
from django.utils import timezone

from transporte.models import Trip
from transporte.serializers.trip import TripSerializer
from transporte.permissions import IsStaffOrReadOnly
from transporte.filters    import TripFilter
from transporte.pagination import StandardPagination


class TripViewSet(viewsets.ModelViewSet):
    serializer_class   = TripSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_class    = TripFilter
    ordering_fields    = ['departure_time', 'price', 'created_at']
    ordering           = ['-departure_time']
    http_method_names  = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        qs = Trip.objects.select_related('bus', 'route', 'driver').prefetch_related('tickets')
        if self.request.user.is_staff:
            return qs.all()
        return qs.filter(status='scheduled')

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser], url_path='start')
    def start(self, request, pk=None):
        trip = self.get_object()
        if trip.status != 'scheduled':
            return Response(
                {'error': f'Cannot start a trip with status "{trip.status}".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        trip.status = 'in_progress'
        trip.save(update_fields=['status'])
        return Response(TripSerializer(trip).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser], url_path='complete')
    def complete(self, request, pk=None):
        trip = self.get_object()
        if trip.status != 'in_progress':
            return Response(
                {'error': f'Cannot complete a trip with status "{trip.status}".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        trip.status = 'completed'
        trip.save(update_fields=['status'])
        return Response(TripSerializer(trip).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser], url_path='cancel')
    def cancel(self, request, pk=None):
        trip = self.get_object()
        if trip.status in ['completed', 'cancelled']:
            return Response(
                {'error': f'Cannot cancel a trip with status "{trip.status}".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        trip.status = 'cancelled'
        trip.save(update_fields=['status'])
        return Response(TripSerializer(trip).data)

    @action(detail=False, methods=['get'], url_path='schedule')
    def schedule(self, request):
        qs = self.filter_queryset(
            self.get_queryset().filter(
                status='scheduled',
                departure_time__gte=timezone.now(),
            )
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                TripSerializer(page, many=True).data
            )
        return Response(TripSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser], url_path='stats')
    def stats(self, request):
        qs = Trip.objects.all()
        totals = qs.aggregate(
            total_trips   = Count('id'),
            total_revenue = Sum('price'),
        )
        by_status = {
            s: qs.filter(status=s).count()
            for s, _ in Trip.STATUS_CHOICES
        }
        return Response({
            'total_trips':  totals['total_trips'],
            'total_revenue': float(totals['total_revenue'] or 0),
            'by_status':    by_status,
        })
