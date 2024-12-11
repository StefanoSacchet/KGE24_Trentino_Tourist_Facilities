import csv
import sys

# Function to add 'id' column to the CSV
def add_id_column(input_file, output_file):
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            rows = list(reader)

            # Check if the file is empty
            if not rows:
                print("Input file is empty.")
                return

            header = rows[0]
            data = rows[1:]

            # Add 'id' to the header
            header.insert(0, 'id')

            # Add incrementing id values to each row
            for i, row in enumerate(data):
                row.insert(0, f"climbing_route{i}")

            # Write the updated data to the output file
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                writer.writerows(data)

        print(f"Updated CSV written to {output_file}.")

    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        add_id_column(input_file, output_file)

