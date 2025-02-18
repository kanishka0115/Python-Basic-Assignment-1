import csv


with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)


column_widths = [max(len(str(item)) for item in column) for column in zip(*rows)]


def print_row(row):
    print(" | ".join(f"{str(item).ljust(width)}" for item, width in zip(row, column_widths)) + " |")

print("+" + "+".join("-" * width for width in column_widths) + "+")

print_row(rows[0])

print("+" + "+".join("-" * width for width in column_widths) + "+")

for row in rows[1:]:
    print_row(row)
print("+" + "+".join("-" * width for width in column_widths) + "+")
