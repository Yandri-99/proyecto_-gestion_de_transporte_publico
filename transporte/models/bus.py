from django.db import models

class Bus(models.Model):
    plate     = models.CharField(max_length=20, unique=True)
    brand     = models.CharField(max_length=50)
    model     = models.CharField(max_length=50)
    year      = models.PositiveIntegerField()
    capacity  = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Bus'
        verbose_name_plural = 'Buses'
        ordering            = ['plate']

    def __str__(self):
        return f'{self.plate} — {self.brand} {self.model}'

    @property
    def available_seats(self):
        from django.utils import timezone
        active_trips = self.trips.filter(
            status__in=['scheduled', 'in_progress'],
            departure_time__gte=timezone.now(),
        )
        booked = sum(
            t.tickets.filter(status='confirmed').count()
            for t in active_trips
        )
        return self.capacity - booked
