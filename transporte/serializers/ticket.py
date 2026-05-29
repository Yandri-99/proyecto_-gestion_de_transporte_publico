from rest_framework import serializers
from transporte.models import Ticket, Trip


class TicketSerializer(serializers.ModelSerializer):
    trip_info   = serializers.SerializerMethodField()
    username    = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model  = Ticket
        fields = [
            'id', 'trip', 'trip_info', 'user', 'username',
            'passenger_name', 'passenger_id', 'seat_number',
            'price', 'status', 'created_at',
        ]
        read_only_fields = ['id', 'user', 'price', 'created_at']

    def get_trip_info(self, obj):
        return {
            'route': f'{obj.trip.route.origin} → {obj.trip.route.destination}',
            'departure': obj.trip.departure_time.isoformat(),
            'bus_plate': obj.trip.bus.plate,
            'driver': str(obj.trip.driver),
        }

    def validate_seat_number(self, value):
        trip = self.initial_data.get('trip')
        if trip:
            try:
                trip_obj = Trip.objects.get(pk=trip)
                if value < 1 or value > trip_obj.bus.capacity:
                    raise serializers.ValidationError(
                        f'Seat number must be between 1 and {trip_obj.bus.capacity}.'
                    )
                if Ticket.objects.filter(trip=trip_obj, seat_number=value, status='confirmed').exists():
                    raise serializers.ValidationError(f'Seat {value} is already taken.')
            except Trip.DoesNotExist:
                pass
        return value

    def validate(self, data):
        trip = data.get('trip')
        if trip and trip.status != 'scheduled':
            raise serializers.ValidationError(
                f'Trip is {trip.status}. Tickets can only be purchased for scheduled trips.'
            )
        return data
