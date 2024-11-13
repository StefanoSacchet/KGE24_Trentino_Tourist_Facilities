import csv
import json

def extract_ski_rental_data(input_data, output_csv):
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "osmId", "name", "coordinates"])

        idPrefix = "ski_rental"
        lineCounter = 0
        for feature in input_data:
            osmId = feature.get("id", "")
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})

            name = properties.get("name", "")
            coordinates = geometry.get("coordinates", [])

            if geometry.get("type") == "Point" and coordinates:
                writer.writerow([idPrefix + str(lineCounter), osmId, name, coordinates])

            lineCounter = lineCounter + 1

if __name__ == "__main__":
    input_data = [
    {
      "type": "Feature",
      "properties": {
        "@id": "node/6466815112",
        "name": "Ski School S. Cristina",
        "shop": "ski_rental"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          11.7258401,
          46.5569714
        ]
      },
      "id": "node/6466815112"
    },
    {
      "type": "Feature",
      "properties": {
        "@id": "node/7047951560",
        "amenity": "ski_school",
        "name": "Ski School & Rental Ortisei",
        "shop": "ski_rental"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          11.6748659,
          46.5765605
        ]
      },
      "id": "node/7047951560"
    },
    {
      "type": "Feature",
      "properties": {
        "@id": "node/7704856850",
        "name": "Maciaconi",
        "shop": "ski_rental"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          11.7284331,
          46.5583359
        ]
      },
      "id": "node/7704856850"
    },
    {
      "type": "Feature",
      "properties": {
        "@id": "node/8794311016",
        "name": "Outdoor Center Rosskopf",
        "shop": "ski_rental"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          11.3973771,
          46.9126212
        ]
      },
      "id": "node/8794311016"
    },
    {
      "type": "Feature",
      "properties": {
        "@id": "node/9196392368",
        "name": "Sportservice Erwin Stricker",
        "name:de": "Sportservice Erwin Stricker",
        "shop": "ski_rental"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          11.737507,
          46.6776077
        ]
      },
      "id": "node/9196392368"
    }
  ]

    output_csv = "ski_rental_data.csv"
    extract_ski_rental_data(input_data, output_csv)
    print(f"Ski rental data extracted and saved to {output_csv}")
