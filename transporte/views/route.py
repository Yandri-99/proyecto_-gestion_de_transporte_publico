from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from transporte.models               import Route
from transporte.serializers.route    import RouteSerializer
from transporte.permissions          import IsStaffOrReadOnly
from transporte.filters              import RouteFilter
from transporte.pagination           import StandardPagination


class RouteViewSet(viewsets.ModelViewSet):
    queryset           = Route.objects.all()
    serializer_class   = RouteSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = RouteFilter
    search_fields      = ['name', 'origin', 'destination']
    ordering_fields    = ['name', 'distance', 'base_price', 'created_at']
    ordering           = ['name']

    @action(detail=True, methods=['get'], url_path='trips')
    def route_trips(self, request, pk=None):
        from transporte.models import Trip
        from transporte.serializers.trip import TripSerializer
        route = self.get_object()
        qs   = route.trips.filter(status__in=['scheduled', 'in_progress']).order_by('departure_time')
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                TripSerializer(page, many=True).data
            )
        return Response(TripSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Route.objects.annotate(num_trips=Count('trips', distinct=True))
        return Response({
            'total':    qs.count(),
            'active':   qs.filter(is_active=True).count(),
            'inactive': qs.filter(is_active=False).count(),
            'detail': [
                {
                    'id':         r.id,
                    'name':       r.name,
                    'origin':     r.origin,
                    'destination': r.destination,
                    'num_trips':  r.num_trips,
                    'is_active':  r.is_active,
                }
                for r in qs.order_by('name')
            ],
        })
