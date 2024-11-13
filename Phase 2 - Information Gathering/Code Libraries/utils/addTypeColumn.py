import csv
import sys

def add_column_with_constant(input_csv, output_csv, constant_value):
    with open(input_csv, mode='r') as infile, open(output_csv, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read header and insert the new column name in the 3rd position (index 2)
        header = next(reader)
        header.insert(1, "type")
        writer.writerow(header)

        # Write each row, inserting the constant value in the 3rd position
        for row in reader:
            row.insert(1, constant_value)
            writer.writerow(row)

    print(f"Updated CSV saved to {output_csv}")

# Usage: python add_column.py <input_csv> <output_csv> <constant_value>
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python add_column.py <input_csv> <output_csv> <constant_value>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    constant_value = sys.argv[3]

    add_column_with_constant(input_csv, output_csv, constant_value)
