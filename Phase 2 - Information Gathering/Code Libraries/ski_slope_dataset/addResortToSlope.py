 
import csv
from geopy.distance import geodesic

# Lista di comprensori sciistici
ski_resorts = [
    {
        "skiResort": "Alba-Ciampac",
        "coordinates": {
            "latitude": 46.452225563775286,
            "longitude": 11.780479349106248
        }
    },
    {
        "skiResort": "Altopiano di Pine'",
        "coordinates": {
            "latitude": 46.16008477044887,
            "longitude": 11.283022235082976
        }
    },
    {
        "skiResort": "Andalo",
        "coordinates": {
            "latitude": 46.1661363,
            "longitude": 11.003402
        }
    },
    {
        "skiResort": "Bellamonte",
        "coordinates": {
            "latitude": 46.3135809,
            "longitude": 11.6623676
        }
    },
    {
        "skiResort": "Bolbeno",
        "coordinates": {
            "latitude": 46.0327428,
            "longitude": 10.7374969
        }
    },
    {
        "skiResort": "Calamento",
        "coordinates": {
            "latitude": 46.131123,
            "longitude": 11.4784937
        }
    },
    {
        "skiResort": "Campitello-Col Rodella",
        "coordinates": {
            "latitude": 46.48515437246003,
            "longitude": 11.748665804511834
        }
    },
    {
        "skiResort": "Canazei-Belvedere",
        "coordinates": {
            "latitude": 46.480286033965136,
            "longitude": 11.804209122054012
        }
    },
    {
        "skiResort": "Cavalese-Cermis",
        "coordinates": {
            "latitude": 46.2510795,
            "longitude": 11.5034071
        }
    },
    {
        "skiResort": "Cermis",
        "coordinates": {
            "latitude": 46.2510795,
            "longitude": 11.5034071
        }
    },
    {
        "skiResort": "Fai",
        "coordinates": {
            "latitude": 46.1793313,
            "longitude": 11.0689304
        }
    },
    {
        "skiResort": "Folgaria",
        "coordinates": {
            "latitude": 45.9149727,
            "longitude": 11.173015
        }
    },
    {
        "skiResort": "Folgarida",
        "coordinates": {
            "latitude": 46.3030712,
            "longitude": 10.8656079
        }
    },
    {
        "skiResort": "Lavarone",
        "coordinates": {
            "latitude": 45.9445551,
            "longitude": 11.2880019
        }
    },
    {
        "skiResort": "Madonna di Campiglio",
        "coordinates": {
            "latitude": 46.2269942,
            "longitude": 10.8270157
        }
    },
    {
        "skiResort": "Marilleva",
        "coordinates": {
            "latitude": 46.30428,
            "longitude": 10.8105041
        }
    },
    {
        "skiResort": "Marmolada",
        "coordinates": {
            "latitude": 46.42436375,
            "longitude": 11.846715936561363
        }
    },
    {
        "skiResort": "Mendola - Roen",
        "coordinates": {
            "latitude": 46.4161297727143,
            "longitude": 11.18858953292481
        }
    },
    {
        "skiResort": "Mendola-Roen",
        "coordinates": {
            "latitude": 46.4161297727143,
            "longitude": 11.18858953292481
        }
    },
    {
        "skiResort": "Moena-Lusia",
        "coordinates": {
            "latitude": 46.3686091,
            "longitude": 11.6853403
        }
    },
    {
        "skiResort": "Molveno",
        "coordinates": {
            "latitude": 46.1421057,
            "longitude": 10.9637773
        }
    },
    {
        "skiResort": "Monte Bondone",
        "coordinates": {
            "latitude": 45.9880488,
            "longitude": 11.0317717
        }
    },
    {
        "skiResort": "Pampeago",
        "coordinates": {
            "latitude": 46.3423281,
            "longitude": 11.5410686
        }
    },
    {
        "skiResort": "Panarotta",
        "coordinates": {
            "latitude": 46.0499949,
            "longitude": 11.3343963
        }
    },
    {
        "skiResort": "Passo Cereda",
        "coordinates": {
            "latitude": 46.1930477,
            "longitude": 11.9054202
        }
    },
    {
        "skiResort": "Passo del Tonale-Presena",
        "coordinates": {
            "latitude": 46.2595849,
            "longitude": 10.584709442007036
        }
    },
    {
        "skiResort": "Passo di Costalunga",
        "coordinates": {
            "latitude": 46.4042798,
            "longitude": 11.6089903
        }
    },
    {
        "skiResort": "Passo Lavazè",
        "coordinates": {
            "latitude": 46.3558474,
            "longitude": 11.485694984374756
        }
    },
    {
        "skiResort": "Passo Rolle",
        "coordinates": {
            "latitude": 46.2964034,
            "longitude": 11.7850596
        }
    },
    {
        "skiResort": "Passo San Pellegrino",
        "coordinates": {
            "latitude": 46.3783576,
            "longitude": 11.7917199
        }
    },
    {
        "skiResort": "Peio",
        "coordinates": {
            "latitude": 46.3628864,
            "longitude": 10.6732435
        }
    },
    {
        "skiResort": "Pian delle Fugazze",
        "coordinates": {
            "latitude": 45.7601964,
            "longitude": 11.1733246
        }
    },
    {
        "skiResort": "Polsa",
        "coordinates": {
            "latitude": 52.215933,
            "longitude": 19.134422
        }
    },
    {
        "skiResort": "Pozza-Buffaure",
        "coordinates": {
            "latitude": 46.4292916481936,
            "longitude": 11.710483238044505
        }
    },
    {
        "skiResort": "Prà Alpesina",
        "coordinates": {
            "latitude": 45.7660886,
            "longitude": 10.866788287834947
        }
    },
    {
        "skiResort": "Predaia",
        "coordinates": {
            "latitude": 46.335273,
            "longitude": 11.0897004
        }
    },
    {
        "skiResort": "Predazzo-Gardone'",
        "coordinates": {
            "latitude": 46.3402748,
            "longitude": 11.577241
        }
    },
    {
        "skiResort": "Ruffre'",
        "coordinates": {
            "latitude": 46.414813,
            "longitude": 11.177774
        }
    },
    {
        "skiResort": "Serrada",
        "coordinates": {
            "latitude": 41.456944,
            "longitude": -4.8625389
        }
    },
    {
        "skiResort": "S. Martino di Castrozza",
        "coordinates": {
            "latitude": 46.2623377,
            "longitude": 11.802828
        }
    },
    {
        "skiResort": "S. Valentino",
        "coordinates": {
            "latitude": 42.7039011,
            "longitude": 11.7380594
        }
    },
    {
        "skiResort": "Tremalzo",
        "coordinates": {
            "latitude": 45.841883,
            "longitude": 10.6866449
        }
    }
]



# Funzione per calcolare la distanza tra due punti (lat, long)
def calculate_distance(point1, point2):
    return geodesic((point1['latitude'], point1['longitude']), (point2['latitude'], point2['longitude'])).kilometers

# Apri il file CSV esistente e leggi i dati
with open('ski_slopes_without_resort.csv', mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Crea una lista per contenere i nuovi dati CSV
updated_rows = []

# Per ogni riga del CSV (ogni pista da sci)
for row in rows:
    # Estrai il primo punto della pista da sci
    trail_coordinates = eval(row['coordinates'])  # Trasforma la stringa di coordinate in lista di tuple
    if isinstance(trail_coordinates[0], float) or isinstance(trail_coordinates[0][1], list):
        continue
    first_point = {'latitude': trail_coordinates[0][1], 'longitude': trail_coordinates[0][0]}  # Punto di partenza della pista

    # Aggiungi una variabile per memorizzare il comprensorio trovato
    ski_resort_found = None

    # Controlla la distanza dal primo punto della pista per ogni comprensorio
    for resort in ski_resorts:
        distance = calculate_distance(first_point, resort['coordinates'])

        if distance < 15:
            ski_resort_found = resort['skiResort']  # Trova il primo comprensorio valido
            break  # Esci dal ciclo, poiché possiamo aggiungere solo un comprensorio per riga

    # Aggiungi il risultato nella colonna "ski_resort" (se trovato, altrimenti lasciamo vuoto)
    row['ski_resort'] = ski_resort_found if ski_resort_found else ''
    updated_rows.append(row)

# Scrivi i dati modificati in un nuovo file CSV
with open('ski_slopes.csv', mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = reader.fieldnames + ['ski_resort']  # Aggiungi la nuova colonna
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()  # Scrivi l'intestazione
    writer.writerows(updated_rows)  # Scrivi i dati modificati
