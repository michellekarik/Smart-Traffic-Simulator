def optimize_traffic(vehicle_counts):
    # Calculate total from all lanes
    total = sum(vehicle_counts.values())
    
    # Determine green light timing based on total vehicles
    if total < 10:
        green = 20
    elif total < 25:
        green = 35
    elif total < 50:
        green = 50
    else:
        green = 70

    # Calculate individual lane timings proportionally
    lane_timings = {}
    if total > 0:
        for lane, count in vehicle_counts.items():
            proportion = count / total
            lane_timings[lane] = round(green * proportion)
    else:
        # Default equal distribution if no vehicles
        num_lanes = len(vehicle_counts)
        for lane in vehicle_counts.keys():
            lane_timings[lane] = round(green / num_lanes) if num_lanes > 0 else 20

    return {
        "green_time_sec": green,
        "red_time_sec": max(20, 90 - green),
        "traffic_level": (
            "Low" if total < 10 else
            "Medium" if total < 25 else
            "High" if total < 50 else
            "Very High"
        ),
        "lane_timings": lane_timings,
        "total_vehicles": total
    }