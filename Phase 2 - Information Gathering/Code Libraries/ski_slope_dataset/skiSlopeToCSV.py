import csv
import json
import sys

def extract_ski_slope_data(input_file, output_csv):
    with open(input_file, 'r') as file:
        data = json.load(file)

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "osmId", "name", "coordinates", "difficulty"])

        idPrefix = "ski_slope"
        lineCounter = 0
        for feature in data:
            osmId = feature.get("id", "");
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})

            name = properties.get("name", "")
            coordinates = geometry.get("coordinates", [])
            difficulty = properties.get("piste:difficulty", "")

            values = [idPrefix + str(lineCounter), osmId, name, coordinates, difficulty]

            if all(values):
                writer.writerow(values)
                lineCounter = lineCounter + 1
            else:
                print(f"Skipping entry without all fields: {osmId}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 skiSlopeToCSV.py <input_file> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]
    extract_ski_slope_data(input_file, output_csv)
    print(f"Ski slope data extracted and saved to {output_csv}")
