import sentence as sen
import even_odd



sentence = input("Enter a sentence= ")
sen.sentence_check(sentence)

numbers = input("Enter numbers separated by commas= ")
num_list = [int(n.strip()) for n in numbers.split(",")]

even, odd = even_odd.count_even_odd(num_list)

print("Even numbers= ", even)
print("Odd numbers= ", odd)

import csv

# a) Read the CSV
filename = "products.csv"

rows = []
with open(filename, "r") as file:
    csvreader = csv.DictReader(file)
    for row in csvreader:
        rows.append(row)

# b) Print each row in clean format
print("\n--- Product List ---")
for r in rows:
    print(f"ID: {r['product_id']}, Name: {r['product_name']}, Category: {r['category']}, "
          f"Price: {r['price']}, Quantity: {r['quantity']}")

# c) Total number of rows
print("\nTotal number of rows:", len(rows))

# d) Total number of products priced above 500
count_above_500 = sum(1 for r in rows if float(r['price']) > 500)
print("Products priced above 500:", count_above_500)

# e) Average price of all products
avg_price = sum(float(r['price']) for r in rows) / len(rows)
print("Average price of all products:", avg_price)

# f) List all products belonging to a specific category
user_cat = input("\nEnter category to filter: ")
print(f"\nProducts in category '{user_cat}':")
for r in rows:
    if r['category'].lower() == user_cat.lower():
        print(f"- {r['product_name']} (Price: {r['price']})")

# g) Total quantity of all items in stock
total_qty = sum(int(r['quantity']) for r in rows)
print("\nTotal quantity of all items in stock:", total_qty)
