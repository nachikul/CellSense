#!/bin/bash
# Script to generate synthetic Excel files using the backend Docker container

echo "Generating synthetic Excel files using backend container..."

# Run the Python script inside the backend container
docker exec cellsense-backend python3 << 'PYTHON_SCRIPT'
import openpyxl
from datetime import datetime, timedelta
import random

def create_synthetic_transactions():
    """Create a well-structured transaction file"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Transactions"
    
    # Headers that the app recognizes well
    headers = ["Date", "Category", "Description", "Amount", "Type"]
    ws.append(headers)
    
    # Income categories
    income_data = [
        ("Salary", "Monthly Salary", 8000),
        ("Salary", "Annual Bonus", 15000),
        ("Investment", "Dividend Payment", 500),
        ("Investment", "Interest Income", 300),
        ("Freelance", "Project Payment", 2500),
    ]
    
    # Expense categories (using keywords the app recognizes)
    expense_data = [
        ("Groceries", "Walmart Shopping", 350),
        ("Groceries", "Whole Foods", 280),
        ("Transportation", "Gas", 60),
        ("Transportation", "Uber Ride", 25),
        ("Dining", "Restaurant Dinner", 85),
        ("Dining", "Coffee Shop", 12),
        ("Utilities", "Electricity Bill", 120),
        ("Utilities", "Internet Bill", 80),
        ("Entertainment", "Movie Tickets", 45),
        ("Entertainment", "Streaming Service", 15),
        ("Healthcare", "Doctor Visit", 150),
        ("Healthcare", "Pharmacy", 45),
        ("Shopping", "Clothing", 200),
        ("Shopping", "Electronics", 500),
        ("Housing", "Rent Payment", 1500),
        ("Loan", "Car Loan Payment", 450),
        ("Loan", "Student Loan", 300),
        ("Savings", "Emergency Fund Deposit", 1000),
        ("Savings", "Investment Deposit", 2000),
        ("Mutual Funds", "Monthly MF Contribution", 5000),
        ("Provident Fund", "EPF Contribution", 12000),
        ("Fixed Deposit", "FD Interest", 500),
        ("Insurance", "Life Insurance Premium", 2500),
    ]
    
    start_date = datetime.now() - timedelta(days=180)
    transactions = []
    
    # Add income entries
    for category, description, amount in income_data:
        for i in range(3):  # Repeat each income type 3 times
            date = start_date + timedelta(days=random.randint(0, 180))
            transactions.append([date.strftime("%Y-%m-%d"), category, description, amount, "Income"])
    
    # Add expense entries
    for category, description, amount in expense_data:
        for i in range(4):  # Repeat each expense type 4 times
            date = start_date + timedelta(days=random.randint(0, 180))
            # Add some variation to amounts
            varied_amount = amount + random.randint(-50, 100)
            transactions.append([date.strftime("%Y-%m-%d"), category, description, varied_amount, "Expense"])
    
    # Sort by date
    transactions.sort(key=lambda x: x[0])
    
    # Add to worksheet
    for row in transactions:
        ws.append(row)
    
    # Save
    wb.save("/app/uploads/synthetic_transactions.xlsx")
    print(f"✓ Created synthetic_transactions.xlsx with {len(transactions)} transactions")
    
    # Calculate totals
    income_total = sum(row[3] for row in transactions if row[4] == "Income")
    expense_total = sum(row[3] for row in transactions if row[4] == "Expense")
    print(f"  Total Income: ${income_total:,.2f}")
    print(f"  Total Expenses: ${expense_total:,.2f}")
    print(f"  Net Balance: ${income_total - expense_total:,.2f}")

if __name__ == "__main__":
    create_synthetic_transactions()
    print("\n✅ File created at /app/uploads/synthetic_transactions.xlsx")
    print("   You can find it in backend/uploads/ directory")
PYTHON_SCRIPT

echo ""
echo "✅ Done! Check backend/uploads/ for synthetic_transactions.xlsx"
