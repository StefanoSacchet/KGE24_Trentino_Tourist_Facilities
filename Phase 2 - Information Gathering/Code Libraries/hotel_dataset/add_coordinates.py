import ssl
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import certifi
import geopy.geocoders
import pandas as pd
from geopy.geocoders import Nominatim

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geolocator = Nominatim(user_agent="crag_locator")

file_path = "hotels.csv"
data = pd.read_csv(file_path, sep=";")


def geocode_address(structure_name, address, municipality):
    query = f"{municipality.lower()}, Trento"
    try:
        location = geolocator.geocode(query, timeout=10)
        if location:
            return (structure_name, address, location.latitude, location.longitude)
        else:
            print(f"Coordinates not found for {query}")
            return (structure_name, address, None, None)
    except Exception as e:
        print(f"Error retrieving coordinates for {structure_name} - {address}: {e}")
        return (structure_name, address, None, None)


structure_positions = {}

# Use ThreadPoolExecutor for parallel geocoding
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [
        executor.submit(
            geocode_address, row["Facility Name"], row["Address"], row["Municipality"]
        )
        for _, row in data.iterrows()
    ]
    for future in as_completed(futures):
        structure_name, address, lat, lon = future.result()
        if lat and lon:
            structure_positions[(structure_name, address)] = (lat, lon)

coordinates_df = pd.DataFrame(
    structure_positions,
    columns=["Municipality", "latitude", "longitude"],
)

data = data.merge(coordinates_df, on=["Municipality"], how="left")

output_path = "hotels_coordinates.csv"
data.to_csv(output_path, index=False, sep=";")
