import ssl
import time

import certifi
import geopy.geocoders
import pandas as pd
from geopy.geocoders import Nominatim

# Load the CSV file
df = pd.read_csv("data/routes_rated.csv")

# Filter rows where the country is "ita" and crag is "arco"
filtered_df = df[df["crag"] == "arco"]

# Load the CSV file
# filtered_df = pd.read_csv("arco_routes_rated.csv")

# Get unique crags
crags = filtered_df["sector"].unique()

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

# Initialize geolocator
geolocator = Nominatim(user_agent="crag_locator")

# Dictionary to store crag coordinates
crag_positions = {}

# Retrieve latitude and longitude for each unique crag
for crag in crags:
    try:
        # Specify the crag location in Arco, Italy
        location = geolocator.geocode(f"{crag}, Trentino, Italy", timeout=10)
        if location:
            crag_positions[crag] = (location.latitude, location.longitude)
            print(
                f"Retrieved coordinates for {crag}: {location.latitude}, {location.longitude}"
            )
        else:
            print(f"Coordinates not found for {crag}")
    except Exception as e:
        print(f"Error retrieving coordinates for {crag}: {e}")
    time.sleep(1)  # Pause to avoid overwhelming the geocoding service

# Convert crag_positions to a DataFrame
crag_df = pd.DataFrame.from_dict(
    crag_positions, orient="index", columns=["latitude", "longitude"]
)
crag_df.reset_index(inplace=True)
crag_df.rename(columns={"index": "sector"}, inplace=True)

# Merge latitude and longitude into the original filtered DataFrame
merged_df = filtered_df.merge(crag_df, on="sector", how="left")

# Save the merged DataFrame to a new CSV file
merged_df.to_csv("data/arco_routes_with_coordinates.csv", index=False)

print("Updated CSV file saved as 'updated_file_with_coordinates.csv'")
