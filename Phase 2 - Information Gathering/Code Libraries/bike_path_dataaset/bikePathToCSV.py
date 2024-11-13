import csv
import json
import requests
from math import radians, sin, cos, sqrt, atan2
import sys

# Function to get elevations for a batch of coordinates
def get_elevations_batch(coordinates):
    locations = [{"latitude": lat, "longitude": lon} for lon, lat in coordinates]
    payload = {"locations": locations}
    url = "https://api.open-elevation.com/api/v1/lookup"

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            return [result["elevation"] for result in data["results"]]
    except Exception as e:
        print(f"Error getting elevation data: {e}")
    return None

# Function to calculate positive elevation gain and distance
def calculate_metrics(coordinates):
    elevations = get_elevations_batch(coordinates)
    if not elevations:
        return None, None

    elevation_gain = 0
    total_distance = 0
    R = 6371000  # Earth’s radius in meters

    for i in range(len(coordinates) - 1):
        lon1, lat1 = map(radians, coordinates[i])
        lon2, lat2 = map(radians, coordinates[i + 1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        total_distance += distance

        elevation_diff = elevations[i + 1] - elevations[i]
        if elevation_diff > 0:
            elevation_gain += elevation_diff

    return elevation_gain, total_distance

# Main function to extract data and create the CSV
def extract_hike_data(input_file, output_csv):
    with open(input_file, 'r') as file:
        data = json.load(file)

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "osmId", "name", "coordinates", "surface", "difficulty", "total_distance_m", "total_elevation_gain_m"])

        idPrefix = "bike"
        lineCounter = 0
        for feature in data:
            osmId = feature.get("id", "")
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})

            name = properties.get("name", "")
            coordinates = geometry.get("coordinates", [])
            surface = properties.get("surface", "")
            difficulty = properties.get("piste:difficulty", "")

            if geometry.get("type") == "LineString" and coordinates:
                elevation_gain, total_distance = calculate_metrics(coordinates)

                if elevation_gain is not None and total_distance is not None:
                    values = [idPrefix + str(lineCounter), osmId, name, coordinates, surface, difficulty, round(total_distance), round(elevation_gain)]

                    # Count empty fields
                    empty_fields_count = sum(1 for value in values if value == "" or value == [])

                    # Keep lines with at most 1 empty field
                    if empty_fields_count <= 1:
                        writer.writerow(values)
                        lineCounter = lineCounter + 1
                    else:
                        print(f"Skipping entry with more than 1 empty field: {osmId}")

# Use the input file and create the CSV file
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 hikeDataExtractor.py <input_file> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]
    extract_hike_data(input_file, output_csv)
    print(f"Hike data extracted and saved to {output_csv}")
