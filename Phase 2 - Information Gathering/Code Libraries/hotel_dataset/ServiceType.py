import csv

def print_unique_service_types(file_path):
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            if 'Service Type' not in reader.fieldnames:
                print("Column 'Service Type' not found in the CSV file.")
                return

            service_types = set()
            for row in reader:
                service_types.add(row['Service Type'])

            print("Unique 'Service Type' values:")
            for service_type in sorted(service_types):
                print(service_type)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example
file_path = 'hotels.csv'  # Replace with the path to your CSV file
print_unique_service_types(file_path)
