# CellSense - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Step 2: Generate Sample Data (Optional)

```bash
cd samples
python create_sample.py
```

This creates `sample_finances.xlsx` with 60 sample transactions.

### Step 3: Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Step 4: Open the Application

Navigate to: http://localhost:3000

### Step 5: Upload Your Data

1. Click "Choose File" or drag and drop your Excel file
2. Your dashboard will load automatically with:
   - Financial summary
   - Interactive charts
   - Searchable transaction table

## 📋 Excel File Format

Your Excel file should have columns like:

| Date       | Category   | Description | Amount | Type    |
|------------|------------|-------------|--------|---------|
| 2024-01-15 | Groceries  | Walmart     | 150.50 | Expense |
| 2024-01-20 | Salary     | Monthly Pay | 5000   | Income  |

**Note:** Column names are flexible - the app auto-detects variations.

## ✨ Features to Try

1. **Customize Layout**: Click "Edit Layout" to drag and resize widgets
2. **Search**: Filter transactions by typing in the search box
3. **Edit Data**: Double-click any cell to edit values
4. **Pagination**: Navigate through large datasets

## 🔧 Troubleshooting

**Backend won't start?**
- Make sure Python 3.9+ is installed
- Check if port 8000 is available

**Frontend won't start?**
- Make sure Node.js 16+ is installed
- Check if port 3000 is available
- Try `rm -rf node_modules && npm install`

**File upload fails?**
- Ensure file is .xlsx or .xls format
- Check file size (keep under 10MB)
- Verify backend is running

## 📊 API Endpoints

- `POST /api/upload` - Upload Excel file
- `GET /api/data/{id}` - Retrieve data
- `POST /api/analyze` - Get detailed analysis

## 💡 Tips

- Use the sample file to understand the expected format
- The app remembers your layout during the session
- Edit mode shows resize handles on widgets
- All data is processed client-side for privacy

---

Need help? Check the main README.md or open an issue!
