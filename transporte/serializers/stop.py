from rest_framework import serializers
from transporte.models import Stop


class StopSerializer(serializers.ModelSerializer):
    route_name = serializers.CharField(source='route.name', read_only=True)

    class Meta:
        model  = Stop
        fields = [
            'id', 'route', 'route_name', 'name', 'address',
            'latitude', 'longitude', 'stop_order', 'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
