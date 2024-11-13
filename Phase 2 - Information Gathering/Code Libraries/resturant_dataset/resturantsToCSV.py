import csv
import json
import sys


def extract_resturant_data(input_file, output_csv):
    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "id",
                "osmId",
                "name",
                "addrCity",
                "addrPostcode",
                "addrStreet",
                "addrHousenumber",
                "phone",
                "latitude",
                "longitude",
            ]
        )

        idPrefix = "resturant"
        lineCounter = 0
        for feature in data:

            osmId = feature.get("id", "")
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})

            name = properties.get("name", "")
            addrCity = properties.get("addr:city", "")
            addrHousenumber = properties.get("addr:housenumber", "")
            addrPostcode = properties.get("addr:postcode", "")
            addrStreet = properties.get("addr:street", "")
            phone = properties.get("contact:phone", "")

            coordinates = geometry.get("coordinates", [])
            lat = coordinates[1] if len(coordinates) > 1 else ""
            lon = coordinates[0] if len(coordinates) > 0 else ""

            values = [
                idPrefix + str(lineCounter),
                osmId,
                name,
                addrCity,
                addrPostcode,
                addrStreet,
                addrHousenumber,
                phone,
                lat,
                lon,
            ]

            # count blanks
            empty_fields_count = sum(
                1 for value in values if value == "" or value == []
            )

            # keep lines with at most 1 blank
            if empty_fields_count <= 1:
                writer.writerow(values)
                lineCounter = lineCounter + 1
            else:
                print(f"Skipping entry with more than 1 empty fields: {osmId}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 resturantToCSV.py <input_file> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]
    extract_resturant_data(input_file, output_csv)
    print(f"Resturant data extracted and saved to {output_csv}")
