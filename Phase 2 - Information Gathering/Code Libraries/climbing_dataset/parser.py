import ssl
import time

import certifi
import geopy.geocoders
import pandas as pd
from geopy.geocoders import Nominatim

df = pd.read_csv("data/routes_rated.csv")
filtered_df = df[df["crag"] == "arco"]

# Update the "sector" column with the modified values
filtered_df["cluster"] = filtered_df["cluster"].apply(lambda x: "cluster-" + str(x))

# Get unique crags
crags = filtered_df["sector"].unique()

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim(user_agent="crag_locator")

crag_positions = {}

# Retrieve latitude and longitude for each unique crag
for crag in crags:
    try:
        location = geolocator.geocode(f"{crag}, Trentino, Italy", timeout=10)
        if location:
            crag_positions[crag] = [location.latitude, location.longitude]
        else:
            print(f"Coordinates not found for {crag}")
    except Exception as e:
        print(f"Error retrieving coordinates for {crag}: {e}")
    time.sleep(1)

crag_df = pd.DataFrame.from_dict(
    crag_positions, orient="index", columns=["latitude", "longitude"]
)
crag_df.reset_index(inplace=True)
crag_df.rename(columns={"index": "sector"}, inplace=True)

crag_df["coordinates"] = crag_df[["latitude", "longitude"]].apply(list, axis=1)

crag_df.drop(columns=["latitude", "longitude"], inplace=True)

merged_df = filtered_df.merge(crag_df, on="sector", how="left")

merged_df.to_csv("data/arco_routes_with_coordinates.csv", index=False)

df = pd.read_csv("data/arco_routes_with_coordinates.csv")

df.drop(columns=["Unnamed: 0"], inplace=True)

# Rename columns
df.rename(columns={"tall_recommend_sum": "height_difficulty_score"}, inplace=True)
df.rename(columns={"cluster": "route_category"}, inplace=True)

# Update values in the column
df["height_difficulty_score"] = df["height_difficulty_score"].map(
    {1: "recommend_high", -1: "recommend_low"}
)
route_category = {
    "cluster-0": "soft_route",
    "cluster-1": "preferred_by_women",
    "cluster-2": "famous_route",
    "cluster-3": "hard_route",
    "cluster-4": "repeated_route",
    "cluster-5": "chipped_route",
    "cluster-6": "non_chipped_route",
    "cluster-7": "easy_on_sight",
    "cluster-8": "less_repeated",
}
df["route_category"] = df["route_category"].map(route_category)

df.to_csv("data/arco_routes_with_coordinates.csv", index=False)
