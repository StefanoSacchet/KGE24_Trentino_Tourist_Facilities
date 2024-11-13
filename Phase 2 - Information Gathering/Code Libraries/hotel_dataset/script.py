import ssl

import certifi
import geopy.geocoders
import pandas as pd
from geopy.geocoders import Nominatim
from googletrans import Translator

file_path = "Provincia-Autonoma-di-Trento---Elenco-strutture-alberghiere.csv"
data = pd.read_csv(file_path, sep=";")

data = data.iloc[:, :27]

# Drop unnecessary columns
data.drop("Denominazione ente annuario", axis=1, inplace=True)
data.drop("Codice esercizio ricettivo", axis=1, inplace=True)
data.drop("Codice localita", axis=1, inplace=True)
data.drop("Codice", axis=1, inplace=True)
data.drop("Frazione", axis=1, inplace=True)
data.drop("FAX", axis=1, inplace=True)
data.drop("Partita IVA", axis=1, inplace=True)
data.drop("Numero unita", axis=1, inplace=True)
data.drop("Posti letto", axis=1, inplace=True)
data.drop("Tipologia unita", axis=1, inplace=True)
data.drop("Prezzo massimo consumazione pasto", axis=1, inplace=True)
data.drop("Prezzo massimo letto aggiunto", axis=1, inplace=True)
data.drop("Tipologia alberghiera", axis=1, inplace=True)
data.drop("Provincia", axis=1, inplace=True)

# Translate rows to english
data["Categoria"] = data["Categoria"].replace(
    {
        "1-stella": "1-star",
        "2-stelle": "2-stars",
        "3-stelle": "3-stars",
        "4-stelle": "4-stars",
        "5-stelle": "5-stars",
        "1-stella-s": "1-star-superior",
        "2-stelle-s": "2-stars-superior",
        "3-stelle-s": "3-stars-superior",
        "4-stelle-s": "4-stars-superior",
        "5-stelle-s": "5-stars-superior",
        "nessuna-stella": "no-stars",
    }
)
data["Tipologia servizio"] = data["Tipologia servizio"].replace(
    {
        "pensione-completa": "full-board",
        "mezza-pensione": "half-board",
        "solo-pernottamento": "room-only",
        "prima-colazione": "bed-and-breakfast",
    }
)

translator = Translator()


def translate_text(text):
    if isinstance(text, str):
        try:
            translated = translator.translate(text, src="it", dest="en")
            if translated and hasattr(translated, "text"):
                return translated.text
            else:
                return text
        except Exception as e:
            print(f"Error translating text '{text}': {e}")
            return text
    return text


# Columns to translate
columns_to_translate = ["Servizi"]

# Apply the translation function
for column in columns_to_translate:
    data[column] = data[column].apply(translate_text)

# Dictionary mapping Italian column names to English
column_translation = {
    "Comune": "Municipality",
    "Provincia": "Province",
    "Categoria": "Star Rating",
    "Denominazione struttura": "Facility Name",
    "Indirizzo": "Address",
    "Frazione": "District",
    "CAP": "Postal Code",
    "Telefono": "Phone",
    "FAX": "Fax",
    "Indirizzo posta elettronica": "Email Address",
    "Sito internet": "Website",
    "Denominazione ente annuario": "Annual Organization Name",
    "Tipologia alberghiera": "Hotel Type",
    "Tipologia servizio": "Service Type",
    "Codice esercizio ricettivo": "Hospitality Code",
    "Partita IVA": "VAT Number",
    "Codice localita": "Location Code",
    "Altitudine": "Altitude",
    "Numero unita": "Number of Units",
    "Numero posti letto": "Number of Beds",
    "Prezzo massimo letto aggiunto": "Max Extra Bed Price",
    "Tipologia unita": "Unit Type",
    "Posti letto": "Beds",
    "Prezzo": "Price",
    "Prezzo massimo consumazione pasto": "Max Meal Price",
    "Codice": "Code",
    "Servizi": "Services",
}

# Rename columns
data.rename(columns=column_translation, inplace=True)

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geolocator = Nominatim(user_agent="crag_locator")

# Add coordinates
structure_positions = {}
total_rows = len(data)
progress_interval = total_rows // 10  # 10% intervals
completed_count = 0
for i, municipality in enumerate(data["Municipality"].unique()):
    try:
        location = geolocator.geocode(f"{municipality.lower()}, Trento", timeout=3)
        if location:
            structure_positions[municipality] = (location.latitude, location.longitude)
        else:
            print(f"Coordinates not found for {municipality}")
    except Exception as e:
        print(f"Error retrieving coordinates for {municipality}: {e}")

    completed_count += 1
    if completed_count % progress_interval == 0:
        print(f"Progress: {completed_count / total_rows * 100:.0f}%")

coord_df = pd.DataFrame.from_dict(
    structure_positions, orient="index", columns=["latitude", "longitude"]
)
coord_df.reset_index(inplace=True)
coord_df.rename(columns={"index": "Municipality"}, inplace=True)

# output_path = "only_coordinates.csv"
# coord_df.to_csv(output_path, index=False, sep=";")

data = data.merge(coord_df, on=["Municipality"], how="left")

# Add unique ID
data.insert(0, "id", ["hotel" + str(i) for i in range(len(data))])

output_path = "hotels.csv"
data.to_csv(output_path, index=False, sep=";")
