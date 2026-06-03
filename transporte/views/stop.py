from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from transporte.models import Stop
from transporte.serializers.stop import StopSerializer
from transporte.permissions import IsStaffOrReadOnly
from transporte.filters import StopFilter
from transporte.pagination import StandardPagination


class StopViewSet(viewsets.ModelViewSet):
    queryset           = Stop.objects.select_related('route').all()
    serializer_class   = StopSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = StopFilter
    search_fields      = ['name', 'address']
    ordering_fields    = ['route', 'stop_order', 'name', 'created_at']
    ordering           = ['route', 'stop_order']
