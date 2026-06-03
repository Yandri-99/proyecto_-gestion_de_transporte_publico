from django.db import models
from .route import Route


class Stop(models.Model):
    route      = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    name       = models.CharField(max_length=100)
    address    = models.CharField(max_length=200)
    latitude   = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude  = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    stop_order = models.PositiveIntegerField(help_text='Order of the stop along the route')
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Stop'
        verbose_name_plural = 'Stops'
        ordering            = ['route', 'stop_order']
        unique_together     = ['route', 'stop_order']

    def __str__(self):
        return f'{self.name} (Stop #{self.stop_order} on {self.route.name})'
