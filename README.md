# CellSense - Interactive Financial Dashboard

An intelligent finance analysis dashboard that transforms your Excel spreadsheets into interactive, visual insights. Upload your financial data and get instant analytics with drag-and-drop customizable widgets.

![CellSense Banner](https://img.shields.io/badge/CellSense-Financial%20Dashboard-blueviolet)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![React](https://img.shields.io/badge/React-18.2-61dafb)

## ✨ Features

- **📊 Excel Upload & Analysis**: Upload any financial Excel sheet and get instant insights
- **🎨 Interactive Dashboard**: Drag-and-drop widgets to customize your view
- **📈 Visual Analytics**: Beautiful charts and graphs (pie charts, bar charts, trends)
- **✏️ Editable Data**: Double-click any cell to edit values on the fly
- **🔍 Smart Search**: Filter and search through your transactions
- **💰 Financial Summary**: Automatic calculation of income, expenses, and balance
- **🤖 AI Financial Assistant**: Ask questions about your finances in plain English
- **🏷️ Custom Keywords**: Add your own financial keywords (Mutual Funds, ESOPS, etc.)
- **🐳 Docker Support**: Easy deployment with Docker and Docker Compose
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nachikul/CellSense.git
cd CellSense
```

2. **Set up the Backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up the Frontend**
```bash
cd ../frontend
npm install
```

### Running the Application

#### Option 1: Docker (Recommended for Production)

```bash
# Quick start with Docker Compose
docker-compose up -d

# Access the application at http://localhost
# Backend API: http://localhost:8000
```

See [DOCKER.md](DOCKER.md) for detailed deployment instructions.

#### Option 2: Local Development

1. **Start the Backend Server**
```bash
cd backend
python main.py
```
The API will be available at `http://localhost:8000`

2. **Start the Frontend (in a new terminal)**
```bash
cd frontend
npm run dev
```
The application will open at `http://localhost:3000`

## 📖 Usage

### 1. Upload Your Excel File

- Click the upload area or drag and drop your Excel file
- Supported formats: `.xlsx`, `.xls`
- The file will be automatically analyzed

### 2. View Your Dashboard

Once uploaded, you'll see:
- **Financial Summary**: Total income, expenses, and net balance
- **Category Charts**: Visual breakdown of your spending
- **Transaction Table**: Searchable, paginated data table

### 3. Customize Your Dashboard

- Click "Edit Layout" to enable drag-and-drop
- Drag widgets by their headers to rearrange
- Resize widgets by dragging the bottom-right corner
- Click "Lock Layout" when done

### 4. Edit Your Data

- Double-click any cell in the transaction table to edit
- Press Enter or click outside to save changes

### 5. Ask AI Questions

- Use the AI Financial Assistant to ask questions in plain English
- Examples: "What's my total income?", "How much did I spend on groceries?"
- Get instant answers based on your financial data

### 6. Use Custom Keywords (Optional)

- Click "Advanced Options" during upload
- Add your own keywords: Mutual Funds, ESOPS, Fixed Deposits, etc.
- The app will detect and highlight these terms in your data

## 📋 Excel File Format

Your Excel file should contain columns like:

| Date       | Category      | Description  | Amount | Type    |
|------------|---------------|--------------|--------|---------|
| 2024-01-15 | Groceries     | Walmart      | 150.50 | Expense |
| 2024-01-20 | Salary        | Monthly Pay  | 5000   | Income  |
| 2024-01-22 | Transportation| Gas          | 45.00  | Expense |

### Required/Recommended Columns:
- **Date**: Transaction date (any common date format)
- **Category**: Type of expense/income
- **Description**: Transaction details
- **Amount**: Transaction amount (numeric)
- **Type**: "Income" or "Expense" (optional)

**Note**: Column names are flexible - the app will auto-detect common variations like "expense", "spending", "cost", "income", "revenue", etc.

### Extended Financial Keywords Support

The app automatically detects these financial terms and more:
- **Investments**: Mutual Funds, Stocks, ESOPS, Fixed Deposits, Recurring Deposits
- **Liabilities**: Loans, Debt, EMI, Credit Card, Mortgage
- **Savings**: Provident Fund (PF/EPF), Savings Account
- **Income**: Salary, Bonus, Dividends, Interest
- **Insurance**: Premium, Policy

You can also add custom keywords during upload for personalized detection.

## 🔧 Sample Data

A sample Excel file is included to help you get started:

```bash
cd samples
python create_sample.py
```

This will generate `sample_finances.xlsx` with 3 months of sample financial data.

## 🏗️ Project Structure

```
CellSense/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── uploads/             # Uploaded files storage
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── FileUpload.jsx
│   │   │   ├── SummaryCard.jsx
│   │   │   ├── ChartWidget.jsx
│   │   │   └── DataTable.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── samples/
│   └── create_sample.py     # Generate sample data
└── README.md
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for Python
- **Pandas**: Data analysis and manipulation
- **OpenPyXL**: Excel file processing
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Recharts**: Charting library
- **React Grid Layout**: Drag-and-drop grid system
- **Axios**: HTTP client

## 📊 API Endpoints

### `POST /api/upload`
Upload and analyze an Excel file
- **Input**: Excel file (.xlsx, .xls), optional custom_keywords
- **Output**: Parsed data and analysis

### `GET /api/data/{data_id}`
Retrieve uploaded data by ID
- **Input**: Data ID
- **Output**: Stored data and analysis

### `POST /api/analyze`
Perform detailed analysis on uploaded data
- **Input**: Data ID
- **Output**: Comprehensive analysis with trends and categories

### `POST /api/ask-ai`
Ask questions about your financial data
- **Input**: Data ID and question in plain English
- **Output**: AI-generated answer with source attribution

## 🎨 Features in Detail

### Drag-and-Drop Dashboard
- Rearrange widgets by dragging their headers
- Resize widgets to your preference
- Layout persists during your session

### Smart Data Analysis
- Automatic detection of financial columns
- Calculation of totals, averages, min/max values
- Category-wise breakdown
- Trend analysis (when date columns are present)
- Extended keyword detection (50+ financial terms)

### AI Financial Assistant
- Natural language question answering
- Rule-based intelligent responses
- Optional AI model integration (Hugging Face)
- Context-aware answers based on your data

### Editable Data Table
- Double-click to edit any cell
- Real-time search and filtering
- Pagination for large datasets
- Sortable columns

## 🔒 Security Notes

- Files are stored temporarily and should be cleared periodically
- No data is permanently stored or shared
- Use HTTPS in production
- Add authentication for multi-user scenarios

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🐛 Known Issues & Roadmap

- [ ] Add data persistence (database)
- [ ] Export modified data back to Excel
- [ ] More chart types (line charts, area charts)
- [ ] Budget tracking and alerts
- [ ] Multi-file comparison
- [ ] Dark mode
- [ ] User authentication
- [ ] Cloud storage integration

## 💬 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ for better financial insights
