from django.db import models
from django.contrib.auth.models import User
from .trip import Trip

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    trip           = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='tickets')
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    passenger_name = models.CharField(max_length=100)
    passenger_id   = models.CharField(max_length=30, help_text='ID or passport number')
    seat_number    = models.PositiveIntegerField()
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['trip', 'seat_number']

    def __str__(self):
        return f'Ticket #{self.id} — {self.passenger_name} (Seat {self.seat_number})'

    @property
    def subtotal(self):
        return float(self.price)
