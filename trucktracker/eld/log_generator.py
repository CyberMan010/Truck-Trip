# eld/log_generator.py
import datetime
from decimal import Decimal

def generate_eld_logs(trip, route_data):
    """
    Generate ELD logs based on the calculated route and stops.
    
    Parameters:
    - trip: Trip model instance
    - route_data: Dictionary with route information and stops
    
    Returns:
    - List of ELD log dictionaries
    """
    logs = []
    
    # Group stops by date
    stops_by_date = {}
    
    for stop in route_data["stops"]:
        arrival_date = stop["arrival_time"].date()
        departure_date = stop["departure_time"].date() if stop["departure_time"] else arrival_date
        
        if arrival_date not in stops_by_date:
            stops_by_date[arrival_date] = []
        
        stops_by_date[arrival_date].append(stop)
        
        # If departure is on a different day, add to that day too
        if departure_date != arrival_date:
            if departure_date not in stops_by_date:
                stops_by_date[departure_date] = []
            stops_by_date[departure_date].append(stop)
    
    # Create a log for each date
    for log_date, stops in stops_by_date.items():
        # Initialize log data structure
        log_data = {
            "date": log_date.strftime("%Y-%m-%d"),
            "driver_name": "Sample Driver",  # In a real app, this would be the actual driver
            "truck_number": "12345",         # In a real app, this would be the actual truck
            "carrier_name": "Sample Carrier", # In a real app, this would be the actual carrier
            "graph_data": [],
            "events": []
        }
        
        # Sort stops by time
        stops.sort(key=lambda x: x["arrival_time"])
        
        # Track duty status throughout the day
        current_status = "OFF"  # Start with OFF duty
        previous_time = datetime.datetime.combine(log_date, datetime.time.min)
        
        # Midnight of the next day
        day_end = datetime.datetime.combine(log_date, datetime.time.max)
        
        # Generate graph data in 15-minute increments
        while previous_time <= day_end:
            # Check if there's a status change
            for stop in stops:
                # If this stop changes our status
                if stop["arrival_time"].date() == log_date and previous_time <= stop["arrival_time"] <= previous_time + datetime.timedelta(minutes=15):
                    if stop["stop_type"] == "START":
                        current_status = "ON"  # On-duty, not driving
                    elif stop["stop_type"] in ["PICKUP", "DROPOFF"]:
                        current_status = "ON"  # On-duty, not driving
                    elif stop["stop_type"] == "FUEL":
                        current_status = "ON"  # On-duty, not driving
                    elif stop["stop_type"] == "REST":
                        current_status = "SB"  # Sleeper berth
                    elif stop["stop_type"] == "SLEEP":
                        current_status = "SB"  # Sleeper berth
                
                # If this stop ends and we start driving
                if stop["departure_time"] and stop["departure_time"].date() == log_date and previous_time <= stop["departure_time"] <= previous_time + datetime.timedelta(minutes=15):
                    if stop["stop_type"] in ["START", "PICKUP", "FUEL", "REST", "SLEEP"]:
                        current_status = "D"  # Driving
            
            # Add data point at this time
            log_data["graph_data"].append({
                "time": previous_time.strftime("%H:%M"),
                "status": current_status
            })
            
            # Move to next 15-minute interval
            previous_time += datetime.timedelta(minutes=15)
        
        # Add events for each stop
        for stop in stops:
            # Only include events that occur on this date
            if stop["arrival_time"].date() <= log_date <= (stop["departure_time"].date() if stop["departure_time"] else stop["arrival_time"].date()):
                event = {
                    "time": stop["arrival_time"].strftime("%H:%M") if stop["arrival_time"].date() == log_date else "00:00",
                    "location": stop["location"],
                    "type": stop["stop_type"]
                }
                log_data["events"].append(event)
                
                # Add departure event if it's on the same day
                if stop["departure_time"] and stop["departure_time"].date() == log_date:
                    departure_event = {
                        "time": stop["departure_time"].strftime("%H:%M"),
                        "location": stop["location"],
                        "type": f"{stop['stop_type']}_DEPARTURE"
                    }
                    log_data["events"].append(departure_event)
        
        # Create the log entry
        logs.append({
            "log_date": log_date,
            "log_data": log_data
        })
    
    return logs