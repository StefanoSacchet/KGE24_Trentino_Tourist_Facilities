import csv
import re

# Input and output file paths
input_file = "hotels.csv"
output_file = "hotels_updated.csv"

# Function to extract house numbers and clean the address
def extract_house_number(address):
    # Match a number (including letters like 15A) after a comma at the end
    match = re.search(r',\s*([\w/]+)$', address)
    if match:
        house_number = match.group(1)
        # Remove the house number and trailing comma from the address
        address = re.sub(r',\s*[\w/]+$', '', address).strip()
        return address, house_number
    return address.strip(), ""  # Return original address and empty house number if no match

# Function to add quotes only if the string contains commas
def format_addr_street(address):
    if ',' in address:
        return f'"{address}"'
    return address

# Read, process, and write the CSV file
with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    # Define the new fieldnames, renaming Address to addrStreet and adding addrHousenumber
    fieldnames = reader.fieldnames[:reader.fieldnames.index('Address')] + \
                 ['addrStreet', 'addrHousenumber'] + \
                 reader.fieldnames[reader.fieldnames.index('Address') + 1:]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    for row in reader:
        # Process the Address column
        addrStreet, addrHousenumber = extract_house_number(row['Address'])
        # Format addrStreet with quotes only if it contains a comma
        row['addrStreet'] = format_addr_street(addrStreet)
        row['addrHousenumber'] = addrHousenumber
        del row['Address']  # Remove the old Address column
        writer.writerow(row)

print(f"Updated file saved as {output_file}")
