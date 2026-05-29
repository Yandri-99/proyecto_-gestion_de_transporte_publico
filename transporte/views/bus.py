from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum

from transporte.models            import Bus
from transporte.serializers.bus   import BusSerializer
from transporte.permissions       import IsStaffOrReadOnly
from transporte.filters           import BusFilter
from transporte.pagination        import StandardPagination


class BusViewSet(viewsets.ModelViewSet):
    queryset           = Bus.objects.all()
    serializer_class   = BusSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = BusFilter
    search_fields      = ['plate', 'brand', 'model']
    ordering_fields    = ['plate', 'brand', 'year', 'capacity', 'created_at']
    ordering           = ['plate']

    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request):
        qs = self.filter_queryset(
            self.get_queryset().filter(is_active=True)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                BusSerializer(page, many=True).data
            )
        return Response(BusSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Bus.objects.all()
        total_capacity = qs.aggregate(total=Sum('capacity'))['total'] or 0
        return Response({
            'total':    qs.count(),
            'active':   qs.filter(is_active=True).count(),
            'inactive': qs.filter(is_active=False).count(),
            'total_capacity': total_capacity,
        })
