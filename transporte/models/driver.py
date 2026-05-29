from django.db import models
from django.contrib.auth.models import User

class Driver(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50, unique=True)
    phone          = models.CharField(max_length=20)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Driver'
        verbose_name_plural = 'Drivers'
        ordering            = ['user__username']

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} — Lic. {self.license_number}'
