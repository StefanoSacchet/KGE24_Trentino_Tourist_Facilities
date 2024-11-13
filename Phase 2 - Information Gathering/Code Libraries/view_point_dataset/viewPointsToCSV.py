import csv
import json
import sys

def extract_view_point_data(input_file, output_csv):
    with open(input_file, 'r') as file:
        data = json.load(file)

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "osmId", "name", "elevation", "coordinates"])

        elevationRows = 0

        idPrefix = "view"
        lineCounter = 0
        for feature in data:
            osmId = feature.get("id", "");
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})

            name = properties.get("name", "")
            elevation = properties.get("ele", "")
            coordinates = geometry.get("coordinates", [])

            values = [idPrefix + str(lineCounter), osmId, name, elevation, coordinates]

            if elevation != "":
                elevationRows = elevationRows + 1

            # count blanks
            empty_fields_count = sum(1 for value in values if value == "" or value == [])

            # keep lines with at most 1 blank
            if empty_fields_count <= 1:
                writer.writerow(values)
                lineCounter = lineCounter + 1
            else:
                print(f"Skipping entry with more than 1 empty fields: {osmId}")

        print(f"elevationRows: {elevationRows}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python viewPointsToCSV.py <input_file> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]
    extract_view_point_data(input_file, output_csv)
    print(f"View point data extracted and saved to {output_csv}")
