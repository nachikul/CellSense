import pandas as pd
from datetime import datetime, timedelta
import random

# Create synthetic financial transaction data
def create_transaction_data():
    """Create transaction-based financial data"""
    transactions = []

    # Income categories
    income_categories = [
        ("Salary", ["Monthly Salary", "Bi-weekly Paycheck", "Annual Bonus"]),
        ("Investment", ["Dividend Payment", "Interest Income", "Capital Gains"]),
        ("Freelance", ["Project Payment", "Consulting Fee", "Contract Work"]),
        ("Other Income", ["Gift", "Refund", "Side Hustle"])
    ]

    # Expense categories
    expense_categories = [
        ("Groceries", ["Walmart", "Whole Foods", "Trader Joe's", "Local Market"]),
        ("Transportation", ["Gas", "Uber", "Public Transit", "Parking", "Car Maintenance"]),
        ("Dining", ["Restaurant", "Coffee Shop", "Fast Food", "Lunch", "Dinner"]),
        ("Utilities", ["Electricity", "Water", "Internet", "Phone", "Gas Bill"]),
        ("Entertainment", ["Movie", "Concert", "Streaming Service", "Games", "Sports"]),
        ("Healthcare", ["Doctor Visit", "Pharmacy", "Insurance Premium", "Gym Membership"]),
        ("Shopping", ["Clothing", "Electronics", "Home Goods", "Books", "Online Purchase"]),
        ("Housing", ["Rent", "Mortgage", "Home Insurance", "Property Tax"]),
        ("Loan", ["Car Loan", "Student Loan", "Personal Loan", "Credit Card Payment"]),
        ("Savings", ["Emergency Fund", "Retirement Contribution", "Investment Deposit"])
    ]

    start_date = datetime.now() - timedelta(days=180)

    # Generate income transactions
    for i in range(15):
        date = start_date + timedelta(days=random.randint(0, 180))
        category, descriptions = random.choice(income_categories)
        description = random.choice(descriptions)
        amount = random.randint(500, 8000) if category == "Salary" else random.randint(50, 2000)
        transactions.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Category": category,
            "Description": description,
            "Amount": amount,
            "Type": "Income"
        })

    # Generate expense transactions
    for i in range(80):
        date = start_date + timedelta(days=random.randint(0, 180))
        category, descriptions = random.choice(expense_categories)
        description = random.choice(descriptions)
        if category == "Housing":
            amount = random.randint(800, 2500)
        elif category == "Loan":
            amount = random.randint(200, 1500)
        elif category == "Savings":
            amount = random.randint(100, 2000)
        else:
            amount = random.randint(10, 500)
        transactions.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Category": category,
            "Description": description,
            "Amount": amount,
            "Type": "Expense"
        })

    # Sort by date
    transactions.sort(key=lambda x: x["Date"])
    return pd.DataFrame(transactions)


# Create investment portfolio data
def create_investment_data():
    """Create investment portfolio data"""
    investments = [
        {
            "Investment Type": "Mutual Funds",
            "Fund Name": "Large Cap Growth Fund",
            "Amount": 50000,
            "Current Value": 52500,
            "Monthly Contribution": 5000,
            "Details": "Aggressive growth strategy"
        },
        {
            "Investment Type": "Mutual Funds",
            "Fund Name": "Index Fund S&P 500",
            "Amount": 75000,
            "Current Value": 81000,
            "Monthly Contribution": 3000,
            "Details": "Low-cost index tracking"
        },
        {
            "Investment Type": "Stocks",
            "Fund Name": "Tech Stock Portfolio",
            "Amount": 30000,
            "Current Value": 34500,
            "Monthly Contribution": 2000,
            "Details": "Individual tech stocks"
        },
        {
            "Investment Type": "Fixed Deposit",
            "Fund Name": "FD - Bank Savings",
            "Amount": 100000,
            "Current Value": 105000,
            "Monthly Contribution": 0,
            "Details": "5% annual interest, 1 year term"
        },
        {
            "Investment Type": "Provident Fund",
            "Fund Name": "EPF Account",
            "Amount": 200000,
            "Current Value": 215000,
            "Monthly Contribution": 12000,
            "Details": "Employer matched contribution"
        },
        {
            "Investment Type": "ESOP",
            "Fund Name": "Employee Stock Options",
            "Amount": 50000,
            "Current Value": 65000,
            "Monthly Contribution": 0,
            "Details": "Vested stock options"
        },
        {
            "Investment Type": "Recurring Deposit",
            "Fund Name": "RD - Monthly Savings",
            "Amount": 25000,
            "Current Value": 26250,
            "Monthly Contribution": 5000,
            "Details": "6% annual interest"
        },
        {
            "Investment Type": "Insurance",
            "Fund Name": "Life Insurance Premium",
            "Amount": 15000,
            "Current Value": 15000,
            "Monthly Contribution": 2500,
            "Details": "Term life insurance policy"
        }
    ]

    return pd.DataFrame(investments)


# Create comprehensive financial data
def create_comprehensive_data():
    """Create a comprehensive financial dataset"""
    data = []

    # Add some investment entries as transactions too
    investments = [
        ("Mutual Funds", "Monthly MF Contribution", 5000),
        ("Mutual Funds", "Index Fund Investment", 3000),
        ("Stocks", "Tech Stock Purchase", 2000),
        ("Provident Fund", "EPF Contribution", 12000),
        ("Fixed Deposit", "FD Maturity Interest", 5000),
        ("Recurring Deposit", "RD Monthly Deposit", 5000),
        ("Insurance", "Life Insurance Premium", 2500)
    ]

    start_date = datetime.now() - timedelta(days=365)

    # Add investment-related transactions
    for investment_type, description, amount in investments:
        for month in range(12):
            date = start_date + timedelta(days=month * 30 + random.randint(0, 5))
            data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Category": investment_type,
                "Description": description,
                "Amount": amount,
                "Type": "Investment"
            })

    # Add regular income
    for month in range(12):
        date = start_date + timedelta(days=month * 30 + 1)
        data.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Category": "Salary",
            "Description": "Monthly Salary",
            "Amount": 8000,
            "Type": "Income"
        })

    # Add expenses
    expense_categories = [
        ("Groceries", 300),
        ("Transportation", 200),
        ("Dining", 400),
        ("Utilities", 250),
        ("Entertainment", 300),
        ("Healthcare", 150),
        ("Shopping", 500),
        ("Housing", 1500),
        ("Loan", 800)
    ]

    for month in range(12):
        for category, base_amount in expense_categories:
            date = start_date + timedelta(days=month * 30 + random.randint(1, 28))
            amount = base_amount + random.randint(-50, 100)
            data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Category": category,
                "Description": f"{category} Payment",
                "Amount": amount,
                "Type": "Expense"
            })

    # Sort by date
    data.sort(key=lambda x: x["Date"])
    return pd.DataFrame(data)


if __name__ == "__main__":
    print("Creating synthetic financial data files...")

    # Create transaction-based file (works best with the app)
    df_transactions = create_transaction_data()
    df_transactions.to_excel("synthetic_transactions.xlsx", index=False, engine="openpyxl")
    print(f"✓ Created synthetic_transactions.xlsx with {len(df_transactions)} transactions")
    print(f"  Columns: {list(df_transactions.columns)}")
    print(f"  Income: ${df_transactions[df_transactions['Type']=='Income']['Amount'].sum():,.2f}")
    print(f"  Expenses: ${df_transactions[df_transactions['Type']=='Expense']['Amount'].sum():,.2f}")

    # Create investment portfolio file
    df_investments = create_investment_data()
    df_investments.to_excel("synthetic_investments.xlsx", index=False, engine="openpyxl")
    print(f"\n✓ Created synthetic_investments.xlsx with {len(df_investments)} investments")
    print(f"  Columns: {list(df_investments.columns)}")
    print(f"  Total Investment Value: ${df_investments['Current Value'].sum():,.2f}")

    # Create comprehensive file
    df_comprehensive = create_comprehensive_data()
    df_comprehensive.to_excel("synthetic_comprehensive.xlsx", index=False, engine="openpyxl")
    print(f"\n✓ Created synthetic_comprehensive.xlsx with {len(df_comprehensive)} records")
    print(f"  Columns: {list(df_comprehensive.columns)}")

    print("\n✅ All synthetic data files created successfully!")
    print("\nRecommended: Try uploading 'synthetic_transactions.xlsx' first - it has the best structure for the app.")
