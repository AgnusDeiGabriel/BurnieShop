import csv

# Read the CSV file
rows = []
with open('products.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Write back without the price column
with open('products.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'image'])
    writer.writeheader()
    for row in rows:
        writer.writerow({'title': row['title'], 'image': row['image']})

print("Prices removed from products.csv")
