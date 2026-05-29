from django.db import models
from .bus import Bus
from .route import Route
from .driver import Driver

class Trip(models.Model):
    STATUS_CHOICES = [
        ('scheduled',   'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed',   'Completed'),
        ('cancelled',   'Cancelled'),
    ]

    bus            = models.ForeignKey(Bus, on_delete=models.PROTECT, related_name='trips')
    route          = models.ForeignKey(Route, on_delete=models.PROTECT, related_name='trips')
    driver         = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='trips')
    departure_time = models.DateTimeField()
    arrival_time   = models.DateTimeField()
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-departure_time']

    def __str__(self):
        return f'Trip #{self.id}: {self.route.origin} → {self.route.destination} ({self.departure_time.date()})'

    @property
    def available_seats(self):
        booked = self.tickets.filter(status='confirmed').count()
        return self.bus.capacity - booked

    @property
    def booked_seats(self):
        return self.tickets.filter(status='confirmed').count()

    @property
    def revenue(self):
        return sum(
            float(t.price)
            for t in self.tickets.filter(status='confirmed')
        )
