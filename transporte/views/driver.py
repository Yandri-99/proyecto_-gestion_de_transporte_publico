from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from transporte.models              import Driver
from transporte.serializers.driver  import DriverSerializer
from transporte.permissions         import IsStaffOrReadOnly
from transporte.filters             import DriverFilter
from transporte.pagination          import StandardPagination


class DriverViewSet(viewsets.ModelViewSet):
    queryset           = Driver.objects.select_related('user').all()
    serializer_class   = DriverSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = DriverFilter
    search_fields      = ['user__username', 'user__first_name', 'user__last_name', 'license_number', 'phone']
    ordering_fields    = ['user__username', 'license_number', 'created_at']
    ordering           = ['user__username']

    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request):
        from transporte.models import Trip
        from django.utils import timezone
        busy_driver_ids = Trip.objects.filter(
            status__in=['scheduled', 'in_progress'],
            departure_time__gte=timezone.now(),
        ).values_list('driver_id', flat=True).distinct()
        qs = self.filter_queryset(
            self.get_queryset().filter(is_active=True).exclude(id__in=busy_driver_ids)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                DriverSerializer(page, many=True).data
            )
        return Response(DriverSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Driver.objects.all()
        return Response({
            'total':    qs.count(),
            'active':   qs.filter(is_active=True).count(),
            'inactive': qs.filter(is_active=False).count(),
        })
