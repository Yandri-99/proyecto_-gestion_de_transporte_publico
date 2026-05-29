from django.contrib import admin
from transporte.models import Route, Bus, Driver, Trip, Ticket


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'origin', 'destination', 'distance', 'base_price', 'is_active']
    list_filter   = ['is_active']
    search_fields = ['name', 'origin', 'destination']


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display  = ['id', 'plate', 'brand', 'model', 'year', 'capacity', 'is_active']
    list_filter   = ['is_active', 'brand']
    search_fields = ['plate', 'brand', 'model']


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'license_number', 'phone', 'is_active']
    list_filter   = ['is_active']
    search_fields = ['user__username', 'license_number']


class TicketInline(admin.TabularInline):
    model  = Ticket
    extra  = 0
    fields = ['passenger_name', 'seat_number', 'price', 'status']


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display    = ['id', 'route', 'bus', 'driver', 'departure_time', 'status']
    list_filter     = ['status', 'route']
    search_fields   = ['route__name', 'bus__plate', 'driver__user__username']
    inlines         = [TicketInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ['id', 'passenger_name', 'trip', 'seat_number', 'price', 'status']
    list_filter   = ['status']
    search_fields = ['passenger_name', 'passenger_id']
