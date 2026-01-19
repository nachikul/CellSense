SYNTHETIC DATA FILES FOR CELLSENSE
===================================

I've created synthetic financial data files that work well with the CellSense app.

OPTION 1: Use the CSV file (Easiest)
-------------------------------------
1. Open "synthetic_transactions.csv" in Excel or Google Sheets
2. Save it as "synthetic_transactions.xlsx" (Excel format)
3. Upload the .xlsx file to CellSense

OPTION 2: Generate Excel file using Docker (Recommended)
----------------------------------------------------------
If your Docker containers are running:

  ./generate_excel.sh

This will create synthetic_transactions.xlsx in backend/uploads/

OPTION 3: Run Python script locally
-----------------------------------
If you have pandas and openpyxl installed:

  python3 create_synthetic_simple.py

FILE STRUCTURE
--------------
The synthetic_transactions.xlsx file contains:
- Date column (YYYY-MM-DD format)
- Category column (recognized financial categories)
- Description column
- Amount column (numeric values)
- Type column (Income/Expense)

KEY FEATURES
------------
✓ Uses financial keywords the app recognizes:
  - Income: Salary, Investment, Freelance
  - Expenses: Groceries, Transportation, Dining, Utilities, etc.
  - Investments: Mutual Funds, Provident Fund, Fixed Deposit, etc.

✓ Proper date formatting
✓ Numeric amounts for calculations
✓ Mix of income and expense transactions
✓ Categories that trigger financial analysis

EXPECTED RESULTS
----------------
When uploaded, you should see:
- Financial Summary with Income/Expenses/Balance
- Charts showing category breakdowns
- Data table with all transactions
- AI assistant can answer questions about your data

Total Income: ~$60,000
Total Expenses: ~$150,000+
Net Balance: Negative (showing expenses > income)
