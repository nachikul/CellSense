import openpyxl
from datetime import datetime, timedelta
import random

# Create a new workbook
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Finances"

# Add headers
headers = ["Date", "Category", "Description", "Amount", "Type"]
ws.append(headers)

# Sample categories and descriptions
expense_categories = [
    ("Groceries", ["Walmart", "Whole Foods", "Trader Joe's", "Local Market"]),
    ("Transportation", ["Gas", "Uber", "Public Transit", "Parking"]),
    ("Dining", ["Restaurant", "Coffee Shop", "Fast Food", "Lunch"]),
    ("Utilities", ["Electricity", "Water", "Internet", "Phone"]),
    ("Entertainment", ["Movie", "Concert", "Streaming Service", "Games"]),
    ("Healthcare", ["Doctor Visit", "Pharmacy", "Insurance", "Gym"]),
    ("Shopping", ["Clothing", "Electronics", "Home Goods", "Books"])
]

income_categories = [
    ("Salary", ["Monthly Salary", "Bonus"]),
    ("Freelance", ["Project Payment", "Consulting Fee"]),
    ("Investment", ["Dividend", "Interest"])
]

# Generate sample data for the last 3 months
start_date = datetime.now() - timedelta(days=90)
data_rows = []

# Add income entries
for i in range(10):
    date = start_date + timedelta(days=random.randint(0, 90))
    category, descriptions = random.choice(income_categories)
    description = random.choice(descriptions)
    amount = random.randint(1000, 5000)
    data_rows.append([date.strftime("%Y-%m-%d"), category, description, amount, "Income"])

# Add expense entries
for i in range(50):
    date = start_date + timedelta(days=random.randint(0, 90))
    category, descriptions = random.choice(expense_categories)
    description = random.choice(descriptions)
    amount = random.randint(20, 500)
    data_rows.append([date.strftime("%Y-%m-%d"), category, description, amount, "Expense"])

# Sort by date
data_rows.sort(key=lambda x: x[0])

# Add to worksheet
for row in data_rows:
    ws.append(row)

# Save the file
wb.save("sample_finances.xlsx")
print("Sample Excel file created: sample_finances.xlsx")
