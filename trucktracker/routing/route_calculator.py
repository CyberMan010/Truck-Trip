# routing/route_calculator.py
import requests
import datetime
import math
from decimal import Decimal

def calculate_route(current_location, pickup_location, dropoff_location, current_cycle_hours):
    """
    Calculate a route including required stops based on HOS regulations.
    
    Parameters:
    - current_location: String of the starting point
    - pickup_location: String of the pickup location
    - dropoff_location: String of the delivery location
    - current_cycle_hours: Decimal of hours already used in the current cycle
    
    Returns:
    - Dictionary with route information and stops
    """
    # Constants for HOS regulations
    MAX_DRIVING_HOURS_PER_DAY = 11
    MAX_ON_DUTY_HOURS_PER_DAY = 14
    MAX_CYCLE_HOURS = 70  # 70 hours / 8 days
    REQUIRED_BREAK_AFTER_HOURS = 8
    REQUIRED_BREAK_LENGTH_HOURS = 0.5
    REQUIRED_RESET_HOURS = 10  # 10-hour reset
    
    # Constants for operations
    AVERAGE_SPEED_MPH = 55
    PICKUP_DROPOFF_HOURS = 1  # 1 hour for pickup/dropoff
    FUEL_STOP_HOURS = 0.5
    MILES_PER_TANK = 1000  # Refuel every 1000 miles
    
    # Get route using OpenRouteService API (free)
    # This is a simplified example - in a real app, you'd use their API
    # For this example, we'll simulate some route data
    
    # Geocode locations to coordinates (simulated)
    locations = {
        "current": {"lat": 40.7128, "lng": -74.0060},  # New York
        "pickup": {"lat": 41.8781, "lng": -87.6298},   # Chicago
        "dropoff": {"lat": 34.0522, "lng": -118.2437}  # Los Angeles
    }
    
    # Calculate distances (simplified)
    distance_to_pickup = 800  # miles (New York to Chicago)
    distance_pickup_to_dropoff = 2100  # miles (Chicago to Los Angeles)
    total_distance = distance_to_pickup + distance_pickup_to_dropoff
    
    # Calculate total driving time
    total_driving_hours = total_distance / AVERAGE_SPEED_MPH
    
    # Initialize result
    now = datetime.datetime.now()
    result = {
        "total_distance": total_distance,
        "total_driving_hours": total_driving_hours,
        "route_coordinates": [],  # In a real app, this would contain the polyline
        "stops": []
    }
    
    # Add current location as starting point
    result["stops"].append({
        "location": current_location,
        "arrival_time": now,
        "departure_time": now,
        "stop_type": "START",
        "latitude": locations["current"]["lat"],
        "longitude": locations["current"]["lng"]
    })
    
    # Track time and HOS
    current_time = now
    hours_available_today = MAX_DRIVING_HOURS_PER_DAY
    hours_since_break = 0
    cycle_hours_used = Decimal(current_cycle_hours)
    
    # Drive to pickup location
    hours_to_pickup = distance_to_pickup / AVERAGE_SPEED_MPH
    distance_covered = 0
    
    while distance_covered < distance_to_pickup:
        # Check if we need a fuel stop
        if distance_covered % MILES_PER_TANK + AVERAGE_SPEED_MPH > MILES_PER_TANK and distance_covered < distance_to_pickup - AVERAGE_SPEED_MPH:
            # Add fuel stop
            fuel_location = f"Fuel stop {len(result['stops'])}"
            current_time += datetime.timedelta(hours=hours_since_break)
            distance_covered += hours_since_break * AVERAGE_SPEED_MPH
            
            # Calculate coordinates (simplified)
            progress = distance_covered / distance_to_pickup
            lat = locations["current"]["lat"] + progress * (locations["pickup"]["lat"] - locations["current"]["lat"])
            lng = locations["current"]["lng"] + progress * (locations["pickup"]["lng"] - locations["current"]["lng"])
            
            result["stops"].append({
                "location": fuel_location,
                "arrival_time": current_time,
                "departure_time": current_time + datetime.timedelta(hours=FUEL_STOP_HOURS),
                "stop_type": "FUEL",
                "latitude": lat,
                "longitude": lng
            })
            
            current_time += datetime.timedelta(hours=FUEL_STOP_HOURS)
            hours_since_break = 0
            cycle_hours_used += Decimal(FUEL_STOP_HOURS)
            continue
        
        # Check if we need a mandatory break
        if hours_since_break >= REQUIRED_BREAK_AFTER_HOURS:
            # Add rest break
            break_location = f"Rest break {len(result['stops'])}"
            current_time += datetime.timedelta(hours=hours_since_break)
            distance_covered += hours_since_break * AVERAGE_SPEED_MPH
            
            # Calculate coordinates (simplified)
            progress = distance_covered / distance_to_pickup
            lat = locations["current"]["lat"] + progress * (locations["pickup"]["lat"] - locations["current"]["lat"])
            lng = locations["current"]["lng"] + progress * (locations["pickup"]["lng"] - locations["current"]["lng"])
            
            result["stops"].append({
                "location": break_location,
                "arrival_time": current_time,
                "departure_time": current_time + datetime.timedelta(hours=REQUIRED_BREAK_LENGTH_HOURS),
                "stop_type": "REST",
                "latitude": lat,
                "longitude": lng
            })
            
            current_time += datetime.timedelta(hours=REQUIRED_BREAK_LENGTH_HOURS)
            hours_since_break = 0
            cycle_hours_used += Decimal(REQUIRED_BREAK_LENGTH_HOURS)
            continue
        
        # Check if we need a reset (end of day)
        hours_left_today = min(hours_available_today, MAX_CYCLE_HOURS - float(cycle_hours_used))
        hours_needed = min(hours_to_pickup - (distance_covered / AVERAGE_SPEED_MPH), REQUIRED_BREAK_AFTER_HOURS - hours_since_break)
        
        if hours_left_today < hours_needed:
            # Add sleep break
            sleep_location = f"Sleep break {len(result['stops'])}"
            current_time += datetime.timedelta(hours=hours_left_today)
            distance_covered += hours_left_today * AVERAGE_SPEED_MPH
            
            # Calculate coordinates (simplified)
            progress = distance_covered / distance_to_pickup
            lat = locations["current"]["lat"] + progress * (locations["pickup"]["lat"] - locations["current"]["lat"])
            lng = locations["current"]["lng"] + progress * (locations["pickup"]["lng"] - locations["current"]["lng"])
            
            result["stops"].append({
                "location": sleep_location,
                "arrival_time": current_time,
                "departure_time": current_time + datetime.timedelta(hours=REQUIRED_RESET_HOURS),
                "stop_type": "SLEEP",
                "latitude": lat,
                "longitude": lng
            })
            
            current_time += datetime.timedelta(hours=REQUIRED_RESET_HOURS)
            hours_available_today = MAX_DRIVING_HOURS_PER_DAY
            hours_since_break = 0
            # After 10-hour reset, we can reduce cycle hours if it's been a full day
            if REQUIRED_RESET_HOURS >= 10:
                cycle_hours_used = max(0, cycle_hours_used - Decimal(24))
            continue
        
        # We can drive for a while
        hours_to_drive = min(hours_needed, hours_left_today)
        current_time += datetime.timedelta(hours=hours_to_drive)
        distance_covered += hours_to_drive * AVERAGE_SPEED_MPH
        hours_since_break += hours_to_drive
        hours_available_today -= hours_to_drive
        cycle_hours_used += Decimal(hours_to_drive)
    
    # Add pickup location
    result["stops"].append({
        "location": pickup_location,
        "arrival_time": current_time,
        "departure_time": current_time + datetime.timedelta(hours=PICKUP_DROPOFF_HOURS),
        "stop_type": "PICKUP",
        "latitude": locations["pickup"]["lat"],
        "longitude": locations["pickup"]["lng"]
    })
    
    current_time += datetime.timedelta(hours=PICKUP_DROPOFF_HOURS)
    hours_since_break += PICKUP_DROPOFF_HOURS
    cycle_hours_used += Decimal(PICKUP_DROPOFF_HOURS)
    
    # Reset for the trip to dropoff
    distance_covered = 0
    
    # Drive to dropoff location using the same logic
    hours_to_dropoff = distance_pickup_to_dropoff / AVERAGE_SPEED_MPH
    
    # Similar logic for the drive to dropoff (simplified for brevity)
    # In a complete implementation, you would repeat the same logic as above
    
    # Add dropoff location (simplified)
    current_time += datetime.timedelta(hours=hours_to_dropoff)
    
    result["stops"].append({
        "location": dropoff_location,
        "arrival_time": current_time,
        "departure_time": current_time + datetime.timedelta(hours=PICKUP_DROPOFF_HOURS),
        "stop_type": "DROPOFF",
        "latitude": locations["dropoff"]["lat"],
        "longitude": locations["dropoff"]["lng"]
    })
    
    return result