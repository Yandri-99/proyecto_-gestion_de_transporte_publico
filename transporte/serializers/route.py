from rest_framework import serializers
from transporte.models import Route


class RouteSerializer(serializers.ModelSerializer):
    total_trips = serializers.SerializerMethodField()

    class Meta:
        model  = Route
        fields = [
            'id', 'name', 'origin', 'destination', 'distance',
            'base_price', 'duration', 'is_active', 'total_trips', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_trips(self, obj):
        return obj.trips.filter(status__in=['scheduled', 'in_progress']).count()
