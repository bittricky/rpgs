import csv
import sys
import argparse

def sort_csv_in_place(input_file, column_name, reverse=False):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        headers = reader.fieldnames
        rows = []

        for row in reader:
            # Clean row by removing unexpected or malformed keys
            cleaned_row = {k: v for k, v in row.items() if k in headers and k is not None}
            if len(cleaned_row) == len(headers):
                rows.append(cleaned_row)
            else:
                print(f"Warning: Skipped malformed row: {row}")

    if column_name not in headers:
        print(f"Error: Column '{column_name}' not found in CSV headers.")
        sys.exit(1)

    def sort_key(row):
        value = row[column_name]
        try:
            return float(value)
        except ValueError:
            return value.lower()

    sorted_rows = sorted(rows, key=sort_key, reverse=reverse)

    with open(input_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(sorted_rows)

    print(f"Sorted '{input_file}' by column '{column_name}'{' (descending)' if reverse else ''}.")

def main():
    parser = argparse.ArgumentParser(description="Sort a CSV file in place by a specified column.")
    parser.add_argument("input_file", help="Path to the CSV file to sort")
    parser.add_argument("column_name", help="Name of the column to sort by")
    parser.add_argument("--desc", action="store_true", help="Sort in descending order")

    args = parser.parse_args()
    sort_csv_in_place(args.input_file, args.column_name, reverse=args.desc)

if __name__ == "__main__":
    main()