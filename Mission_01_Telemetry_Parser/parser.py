#!/usr/bin/env python3

from pydantic import BaseModel, Field, ValidationError

class TelemetryPacket(BaseModel):
    timestamp: str
    altitude_m: float = Field(ge=0)
    velocity_ms: float
    fuel_level: float = Field(ge=0, le=100)

def parse_telemetry(data_string):
    try:
        parts = data_string.split("|")
        
        # Dictionary where keys match the Class attributes exactly
        telemetry = {
            "timestamp": parts[0],
            "altitude_m": parts[1],
            "velocity_ms": parts[2],
            "fuel_level": parts[3] 
        }

        # The '**' unpacks the dict into the Class constructor
        validated_packet = TelemetryPacket(**telemetry)

        # We return the object itself
        return validated_packet

    except (IndexError, ValueError, ValidationError):
        return None

def print_mission_summary(total_alt, count):
    if count > 0:
        average_altitude_ft = total_alt / count
        print(f"Average altitude: {average_altitude_ft:.2f}ft")
    else:
        print("No valid packets to average.")

def main():
    flight_log = [
        "2026-04-29T10:00:01|500|150|99",
        "2026-04-29T10:00:02|1200|300|98",
        "2026-04-29T10:00:03|2500|500|97",
        "2026-04-29T10:00:04|NO DATA FOUND",
        "2026-04-29T10:00:05|5000|800|95"
    ]

    print(f"--- Initiating Log Processing: {len(flight_log)} Packets Found ---")

    total_altitude = 0
    valid_packet_count = 0

    for packet in flight_log:
        result = parse_telemetry(packet)
        
        if result:
            # IMPORTANT: Use .attribute notation, not ['key']
            # We do the unit conversion here in the logic layer
            alt_ft = result.altitude_m * 3.28
            
            print(f"Time: {result.timestamp} | Alt: {alt_ft:.2f}ft")

            total_altitude += alt_ft
            valid_packet_count += 1
        else:
            print("System Alert: Skipping corrupted packet...")

    print_mission_summary(total_altitude, valid_packet_count)
                
if __name__ == "__main__":
    main()