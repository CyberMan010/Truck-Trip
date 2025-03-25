# api/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Trip, RouteStop, EldLog
from .serializers import TripSerializer, RouteStopSerializer, EldLogSerializer
from routing.route_calculator import calculate_route
from eld.log_generator import generate_eld_logs

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trip = serializer.save()
        
        # Calculate route and generate stops
        route_data = calculate_route(
            trip.current_location,
            trip.pickup_location,
            trip.dropoff_location,
            trip.current_cycle_hours
        )
        
        # Create stops
        for stop_data in route_data['stops']:
            RouteStop.objects.create(trip=trip, **stop_data)
        
        # Generate ELD logs
        eld_logs = generate_eld_logs(trip, route_data)
        for log_data in eld_logs:
            EldLog.objects.create(trip=trip, **log_data)
        
        # Refresh trip data to include stops and logs
        trip = Trip.objects.get(pk=trip.pk)
        return Response(TripSerializer(trip).data, status=status.HTTP_201_CREATED)