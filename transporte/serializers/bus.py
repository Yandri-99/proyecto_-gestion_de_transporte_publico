from rest_framework import serializers
from transporte.models import Bus


class BusSerializer(serializers.ModelSerializer):
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model  = Bus
        fields = [
            'id', 'plate', 'brand', 'model', 'year',
            'capacity', 'available_seats', 'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_available_seats(self, obj):
        return obj.available_seats

    def validate_plate(self, value):
        qs = Bus.objects.filter(plate__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A bus with this plate already exists.')
        return value.upper()
