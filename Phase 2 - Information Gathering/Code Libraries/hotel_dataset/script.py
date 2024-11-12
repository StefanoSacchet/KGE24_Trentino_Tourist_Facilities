import pandas as pd
from googletrans import Translator

# Load the dataset
file_path = "Provincia-Autonoma-di-Trento---Elenco-strutture-alberghiere.csv"
data = pd.read_csv(file_path, sep=";")

# Select only the first 27 columns
data = data.iloc[:, :27]

# Drop unnecessary columns
data.drop("Denominazione ente annuario", axis=1, inplace=True)
data.drop("Codice esercizio ricettivo", axis=1, inplace=True)
data.drop("Codice localita", axis=1, inplace=True)
data.drop("Codice", axis=1, inplace=True)

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
data["Tipologia alberghiera"] = data["Tipologia alberghiera"].replace(
    {
        "albergo": "hotel",
        "rta": "tourist hotel residence",
        "garni": "hotel",
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
data["Tipologia unita"] = data["Tipologia unita"].replace(
    {
        "camera-senza-bagno": "room-without-bathroom",
        "camera-con-bagno": "room-with-bathroom",
        "appartamento": "apartment",
        "bicamera-con-bagno": "two-room-with-bathroom",
    }
)

# Initialize the translator
translator = Translator()


def translate_text(text):
    if isinstance(text, str):  # Only translate if the cell contains text
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
    "Categoria": "Category",
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

# Save the filtered data
output_path = "hotels.csv"
data.to_csv(output_path, index=False, sep=";")
