# api/serializers.py
from rest_framework import serializers
from .models import Trip, RouteStop, EldLog

class RouteStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStop
        fields = ['id', 'location', 'arrival_time', 'departure_time', 'stop_type', 'latitude', 'longitude']

class EldLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EldLog
        fields = ['id', 'log_date', 'log_data']

class TripSerializer(serializers.ModelSerializer):
    stops = RouteStopSerializer(many=True, read_only=True)
    eld_logs = EldLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = ['id', 'current_location', 'pickup_location', 'dropoff_location', 
                  'current_cycle_hours', 'created_at', 'stops', 'eld_logs']