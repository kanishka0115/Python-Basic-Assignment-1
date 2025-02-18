import csv
json_data = {
    "orders": [
        {
            "order_id": "O001",
            "customer": {"id": "C001", "name": "John Doe", "email": "john@example.com"},
            "items": [
                {"product_id": "P001", "name": "Laptop", "price": 999.99, "quantity": 1},
                {"product_id": "P002", "name": "Mouse", "price": 25.99, "quantity": 2}
            ],
            "shipping_address": "123 Main St, Springfield, IL"
        },
        {
            "order_id": "O002",
            "customer": {"id": "C002", "name": "Jane Smith", "email": "jane@example.com"},
            "items": [
                {"product_id": "P003", "name": "Phone", "price": 599.99, "quantity": 1}
            ],
            "shipping_address": "456 Oak St, Seattle, WA"
        },
        {
            "order_id": "O003",
            "customer": {"id": "C001", "name": "John Doe", "email": "john@example.com"},
            "items": [
                {"product_id": "P004", "name": "Headphones", "price": 149.99, "quantity": 1},
                {"product_id": "P005", "name": "Keyboard", "price": 99.99, "quantity": 1}
            ],
            "shipping_address": "123 Main St, Springfield, IL"
        }
    ]
}


orders = json_data["orders"]
processed_orders = []



for order in orders:
    order_id = order["order_id"]              
    customer_name = order["customer"]["name"]
    shipping_address = order["shipping_address"]

    for item in order["items"]:
        product_name = item["name"]
        price = item["price"]
        quantity = item["quantity"]

        total_value = price * quantity
        discount = total_value * 0.1 if total_value > 100 else 0
        shipping_cost = quantity * 5
        final_total = total_value - discount + shipping_cost

        processed_orders.append([
            order_id, customer_name, product_name, price, quantity,
            total_value, discount, shipping_cost, final_total, shipping_address
        ])
csv_filename = "processed_sales.csv"
with open(csv_filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Order ID", "Customer Name", "Product Name", "Product Price", 
                     "Quantity Purchased", "Total Value", "Discount", 
                     "Shipping Cost", "Final Total", "Shipping Address"])
    writer.writerows(processed_orders)

print(f"Processed data saved to {csv_filename}")