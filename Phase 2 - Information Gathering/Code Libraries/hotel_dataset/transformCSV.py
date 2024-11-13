import csv
import sys

def convert_csv(input_file, output_file):
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=',')

        # Copy all rows from input to output, changing the delimiter
        for row in reader:
            writer.writerow(row)

    print(f"CSV file has been converted and saved to {output_file}")

# Usage: python convert_csv.py <input_file> <output_file>
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_csv.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_csv(input_file, output_file)
