#!/usr/bin/env python3

# Parses raw data and sets up telemetry dictionary
def parse_telemetry(data_string):
    """
    Parses a pipe-delimited telemetry string into a dictionary.
    
    Args:
        data_string (str): A string in 'ISO8601|Alt|Vel|Fuel' format.
        
    Returns:
        dict: Parsed telemetry with unit conversions, or None if corrupted.
    """
    try:
        parts = data_string.split("|")
        
        alt_m = int(parts[1])
        alt_ft = round(alt_m * 3.28, 2)
        
        telemetry = {
            "timestamp": parts[0],
            "altitude_m": int(parts[1]),
            "altitude_ft": alt_ft,
            "velocity_ms": int(parts[2]),
            "fuel_percent": int(parts[3])
        }
        return telemetry

    # Error handling - missing packets/corrupted data
    except IndexError:
        print("[ERROR] Telemetry Packet Corrupted: Missing data fields.")
        return None
    except ValueError:
        print("[ERROR] Telemetry Packet Corrupted: Non-numeric data in numeric field.")
        return None

def print_mission_summary(total_alt, count):
    average_altitude_ft = total_alt / count
    print(f"Average altitude: {average_altitude_ft}ft")


def main():
    # A list representing a stream of incoming satellite data
    flight_log = [
        "2026-04-29T10:00:01|500|150|99",
        "2026-04-29T10:00:02|1200|300|98",
        "2026-04-29T10:00:03|2500|500|97",
        "2026-04-29T10:00:04|NO DATA FOUND", # This tests error handling!
        "2026-04-29T10:00:05|5000|800|95"
    ]

    print(f"--- Initiating Log Processing: {len(flight_log)} Packets Found ---")

    total_altitude = 0
    valid_packet_count = 0

    # The Loop: 'packet' is a temporary variable for the current item
    for packet in flight_log:
        result = parse_telemetry(packet)
        
        if result:
            # If data is valid, print the result
            print(f"Time: {result['timestamp']} | Alt: {result['altitude_ft']}ft")

            # If data is valid, update total altitude and valid packet count
            total_altitude += result['altitude_ft']
            valid_packet_count += 1

        else:
            # If parse_telemetry returned None (due to an error), we skip it
            print("System Alert: Skipping corrupted packet...")

    print_mission_summary(total_altitude, valid_packet_count)
                
if __name__ == "__main__":
    main()