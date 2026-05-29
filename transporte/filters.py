import django_filters
from django.db import models
from transporte.models import Route, Bus, Driver, Trip, Ticket


class RouteFilter(django_filters.FilterSet):
    name        = django_filters.CharFilter(lookup_expr='icontains')
    origin      = django_filters.CharFilter(lookup_expr='icontains')
    destination = django_filters.CharFilter(lookup_expr='icontains')
    price_min   = django_filters.NumberFilter(field_name='base_price', lookup_expr='gte')
    price_max   = django_filters.NumberFilter(field_name='base_price', lookup_expr='lte')

    class Meta:
        model  = Route
        fields = ['is_active', 'origin', 'destination']


class BusFilter(django_filters.FilterSet):
    plate        = django_filters.CharFilter(lookup_expr='icontains')
    brand        = django_filters.CharFilter(lookup_expr='icontains')
    capacity_min = django_filters.NumberFilter(field_name='capacity', lookup_expr='gte')
    capacity_max = django_filters.NumberFilter(field_name='capacity', lookup_expr='lte')

    class Meta:
        model  = Bus
        fields = ['is_active', 'brand', 'year']


class DriverFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model  = Driver
        fields = ['is_active']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(user__username__icontains=value) |
            models.Q(user__first_name__icontains=value) |
            models.Q(user__last_name__icontains=value) |
            models.Q(license_number__icontains=value)
        )


class TripFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='departure_time', lookup_expr='date__gte')
    to_date   = django_filters.DateFilter(field_name='departure_time', lookup_expr='date__lte')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model  = Trip
        fields = ['status', 'route', 'bus', 'driver']


class TicketFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    to_date   = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model  = Ticket
        fields = ['status', 'trip', 'seat_number']
