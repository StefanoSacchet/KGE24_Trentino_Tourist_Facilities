import json
import requests
from time import sleep

# Function to get coordinates from a place name using the Nominatim API
def get_coordinates(place_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {place_name}: {e}")
    return None, None

# Function to create a list of dictionaries with "skiResort" and "coordinates"
def create_location_list(locations):
    place_list = []
    for location in locations:
        place_name = location["LOCALITA'"]
        
        # Check if we have already fetched this place name
        if not any(entry["skiResort"] == place_name for entry in place_list):
            lat, lon = get_coordinates(place_name)
            if lat is not None and lon is not None:
                place_list.append({
                    "skiResort": place_name,
                    "coordinates": {
                        "latitude": lat,
                        "longitude": lon
                    }
                })
            # Add a short delay to avoid overwhelming the server
            sleep(2)
    
    return place_list

# Function to read input data from a JSON file
def read_locations_from_file(filename):
    with open(filename, "r", encoding="latin1") as file:  # Adjust encoding if needed
        return json.load(file)

# Function to save the place-to-coordinates list to a JSON file
def save_location_list_to_file(place_list, output_filename):
    with open(output_filename, "w", encoding="utf-8") as file:
        json.dump(place_list, file, ensure_ascii=False, indent=4)

# Example usage
if __name__ == "__main__":
    # Load data from input file
    locations = read_locations_from_file("datiOpenSkiSlopes.json")
    
    # Create the place-to-coordinates list
    place_list = create_location_list(locations)
    
    # Save the place list to a JSON file
    save_location_list_to_file(place_list, "skiResortCoords.json")
    
    print("Place-to-coordinates list saved to skiResortCoords.json")

