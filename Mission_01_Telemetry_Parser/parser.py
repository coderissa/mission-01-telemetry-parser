#!/usr/bin/env python3

def parse_telemetry(data_string):
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

    except IndexError:
        print("[ERROR] Telemetry Packet Corrupted: Missing data fields.")
        return None
    except ValueError:
        print("[ERROR] Telemetry Packet Corrupted: Non-numeric data in numeric field.")
        return None

def main():
    # TEST 1: Perfect Data
    print("--- Testing Mission Nominal Data ---")
    raw_data = "2026-04-28T09:00:00|42000|7500|88"
    result = parse_telemetry(raw_data)
    if result:
        print(f"Altitude: {result['altitude_m']}m | Fuel: {result['fuel_percent']}%")

    # TEST 2: Broken Data (Missing the fuel field)
    print("\n--- Testing Corrupted Data ---")
    broken_data = "2026-04-28T09:00:00|42000|7500|abc" 
    parse_telemetry(broken_data)

    # Checking conversion from m to feet
    print("\n--- Feet and Meters ---")
    if result:
        print(f"Altitude in meters: {result['altitude_m']}m | Altitude in feet: {result['altitude_ft']}ft")
    

if __name__ == "__main__":
    main()