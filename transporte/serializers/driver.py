from rest_framework import serializers
from django.contrib.auth.models import User
from transporte.models import Driver


class DriverSerializer(serializers.ModelSerializer):
    username    = serializers.CharField(source='user.username', read_only=True)
    full_name   = serializers.SerializerMethodField()

    class Meta:
        model  = Driver
        fields = [
            'id', 'user', 'username', 'full_name',
            'license_number', 'phone', 'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def validate_license_number(self, value):
        qs = Driver.objects.filter(license_number__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A driver with this license already exists.')
        return value.upper()
