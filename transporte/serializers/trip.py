from rest_framework import serializers
from transporte.models import Trip


class TripSerializer(serializers.ModelSerializer):
    route_name     = serializers.CharField(source='route.name', read_only=True)
    bus_plate      = serializers.CharField(source='bus.plate', read_only=True)
    driver_name    = serializers.SerializerMethodField()
    available_seats = serializers.SerializerMethodField()
    booked_seats   = serializers.SerializerMethodField()
    revenue        = serializers.SerializerMethodField()

    class Meta:
        model  = Trip
        fields = [
            'id', 'route', 'route_name', 'bus', 'bus_plate',
            'driver', 'driver_name', 'departure_time', 'arrival_time',
            'price', 'status', 'available_seats', 'booked_seats',
            'revenue', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_driver_name(self, obj):
        return str(obj.driver)

    def get_available_seats(self, obj):
        return obj.available_seats

    def get_booked_seats(self, obj):
        return obj.booked_seats

    def get_revenue(self, obj):
        return obj.revenue

    def validate(self, data):
        if data.get('departure_time') and data.get('arrival_time'):
            if data['arrival_time'] <= data['departure_time']:
                raise serializers.ValidationError(
                    'Arrival time must be after departure time.'
                )
        return data
