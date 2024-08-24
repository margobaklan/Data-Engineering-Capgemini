import numpy as np

def print_array(array, message=""):
    if message:
        print(message)
    print(array)
    print()

# e-commerce transactions
# transaction_id, user_id, product_id, quantity, price, timestamp
transactions = np.array([
    [1, 101, 501, 2, 19.99, '2024-08-01'],
    [2, 102, 502, 1, 29.99, '2024-08-01'],
    [3, 101, 501, 3, 19.99, '2024-08-02'],
    [4, 103, 503, 0, 39.99, '2024-08-02'],
    [5, 104, 504, 4, 9.99, '2024-08-03'],
    [6, 105, 505, 7, 49.99, '2024-08-03'],
    [7, 103, 506, 8, 50.99, '2024-08-04'],
    [8, 104, 507, 7, 119.99, '2024-08-04']
], dtype=object)

print_array(transactions, "Transactions:")

# Total Revenue Function
def total_revenue(transactions):
    quantities = transactions[:, 3].astype(float)
    prices = transactions[:, 4].astype(float)
    revenue = np.sum(quantities * prices)
    return revenue

# Unique Users Function
def unique_users(transactions):
    unique_user_ids = np.unique(transactions[:, 1])
    return unique_user_ids.size

# Most Purchased Product Function
def most_purchased_product(transactions):
    product_quantities = {}
    for transaction in transactions:
        product_id = transaction[2]
        quantity = int(transaction[3])
        if product_id in product_quantities:
            product_quantities[product_id] += quantity
        else:
            product_quantities[product_id] = quantity
    most_purchased = max(product_quantities, key=product_quantities.get)
    return most_purchased

# Convert the price from float to integer
def convert_price_to_int(transactions):
    transactions[:, 4] = transactions[:, 4].astype(float).astype(int)
    return transactions

# Check the data types of each column
def check_data_types(transactions):
    return [transactions[:, i].dtype for i in range(transactions.shape[1])]

# Product Quantity Array Function
def product_quantity_array(transactions):
    return transactions[:, [2, 3]]

# User Transaction Count Function
def user_transaction_count(transactions):
    unique_users, counts = np.unique(transactions[:, 1], return_counts=True)
    return np.column_stack((unique_users, counts))

# Masked Array Function
def masked_array(transactions):
    mask = transactions[:, 3].astype(int) != 0
    return transactions[mask]

# Price Increase Function
def increase_price(transactions, percentage):
    transactions[:, 4] = (transactions[:, 4].astype(float) * (1 + percentage / 100)).astype(float)
    return transactions

# Filter Transactions Function
def filter_transactions(transactions):
    return transactions[transactions[:, 3].astype(int) > 1]

# Revenue Comparison Function
def revenue_comparison(transactions, start_date1, end_date1, start_date2, end_date2):
    date_mask1 = (transactions[:, 5] >= start_date1) & (transactions[:, 5] <= end_date1)
    date_mask2 = (transactions[:, 5] >= start_date2) & (transactions[:, 5] <= end_date2)
    
    revenue1 = total_revenue(transactions[date_mask1])
    revenue2 = total_revenue(transactions[date_mask2])
    
    return revenue1, revenue2

# User Transactions Function
def user_transactions(transactions, user_id):
    return transactions[transactions[:, 1] == user_id]

# Date Range Slicing Function
def date_range_slicing(transactions, start_date, end_date):
    date_mask = (transactions[:, 5] >= start_date) & (transactions[:, 5] <= end_date)
    return transactions[date_mask]

# Top Products Function
def top_products(transactions, top_n=5):
    quantities = transactions[:, 3].astype(float)
    prices = transactions[:, 4].astype(float)
    revenues = quantities * prices
    
    product_revenue = {}
    for product_id, revenue in zip(transactions[:, 2], revenues):
        if product_id in product_revenue:
            product_revenue[product_id] += revenue
        else:
            product_revenue[product_id] = revenue
    
    top_products = sorted(product_revenue, key=product_revenue.get, reverse=True)[:top_n]
    top_transactions = transactions[np.isin(transactions[:, 2], top_products)]
    
    return top_transactions

# Output total revenue
revenue = total_revenue(transactions)
print_array(revenue, "Total Revenue:")

# Output unique users
unique_user_count = unique_users(transactions)
print_array(unique_user_count, "Number of Unique Users:")

# Output most purchased product
most_purchased = most_purchased_product(transactions)
print_array(most_purchased, "Most Purchased Product:")

# Convert price to integer and check data types
transactions = convert_price_to_int(transactions)
print_array(transactions, "Transactions with price converted to integer:")

data_types = check_data_types(transactions)
print_array(data_types, "Data Types of each column:")

# Output product quantity array
product_quantity = product_quantity_array(transactions)
print_array(product_quantity, "Product Quantity Array:")

# Output user transaction counts
transaction_counts = user_transaction_count(transactions)
print_array(transaction_counts, "User Transaction Counts:")

# Output masked array with non-zero quantities
masked = masked_array(transactions)
print_array(masked, "Masked Array with non-zero quantities:")

# Increase prices by 5%
transactions = increase_price(transactions, 5)
print_array(transactions, "Transactions with prices increased by 5%:")

# Filter transactions with quantity > 1
filtered_transactions = filter_transactions(transactions)
print_array(filtered_transactions, "Filtered Transactions with quantity > 1:")

# Revenue comparison between two periods
revenue1, revenue2 = revenue_comparison(transactions, '2024-08-01', '2024-08-02', '2024-08-02', '2024-08-03')
print_array(revenue1, "Revenue from Period 1:")
print_array(revenue2, "Revenue from Period 2:")

# Output transactions for a specific user
user_trans = user_transactions(transactions, 101)
print_array(user_trans, "Transactions for User 101:")

# Output transactions within a specific date range
date_range_trans = date_range_slicing(transactions, '2024-08-01', '2024-08-02')
print_array(date_range_trans, "Transactions within Date Range 2024-08-01 to 2024-08-02:")

# Output top 5 products by revenue
top_products_by_revenue = top_products(transactions)
print_array(top_products_by_revenue, "Transactions of the top 5 Products by Revenue:")

# Verification
assert transactions.shape[1] == 6, "The array should have 6 columns."
assert masked.shape[0] == np.sum(transactions[:, 3].astype(int) > 0), "Masked array should match transactions with non-zero quantities."
