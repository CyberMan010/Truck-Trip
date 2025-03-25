# api/models.py
from django.db import models

class Trip(models.Model):
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    current_cycle_hours = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Trip from {self.pickup_location} to {self.dropoff_location}"

class RouteStop(models.Model):
    trip = models.ForeignKey(Trip, related_name='stops', on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField(null=True, blank=True)
    stop_type = models.CharField(max_length=50, choices=[
        ('PICKUP', 'Pickup'),
        ('DROPOFF', 'Dropoff'),
        ('REST', 'Rest Break'),
        ('SLEEP', 'Sleep Break'),
        ('FUEL', 'Fueling')
    ])
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return f"{self.get_stop_type_display()} at {self.location}"

class EldLog(models.Model):
    trip = models.ForeignKey(Trip, related_name='eld_logs', on_delete=models.CASCADE)
    log_date = models.DateField()
    log_data = models.JSONField()  # Store the structured log data
    
    def __str__(self):
        return f"ELD Log for {self.trip} on {self.log_date}"