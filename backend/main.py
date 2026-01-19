from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import os
import json
from datetime import datetime
import uuid
import httpx

app = FastAPI(title="CellSense API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Store uploaded data in memory for this session
data_store = {}

# Extended financial keywords
FINANCIAL_KEYWORDS = [
    'mutual funds', 'mutual fund', 'mf', 'savings', 'loan', 'loans',
    'liability', 'liabilities', 'provident fund', 'pf', 'epf',
    'debt', 'debts', 'fixed deposit', 'fd', 'recurring deposit', 'rd',
    'stock', 'stocks', 'equity', 'esop', 'esops', 'employee stock',
    'investment', 'investments', 'asset', 'assets', 'insurance',
    'premium', 'dividend', 'dividends', 'interest', 'emi', 'credit card',
    'debit card', 'mortgage', 'rent', 'salary', 'bonus', 'income',
    'expense', 'revenue', 'profit', 'loss', 'tax', 'taxes'
]

class AIQuestionRequest(BaseModel):
    data_id: str
    question: str

class UploadRequest(BaseModel):
    custom_keywords: Optional[List[str]] = None


def _dedupe_columns(names: List[str]) -> List[str]:
    seen = {}
    deduped = []
    for name in names:
        base = str(name).strip()
        if not base:
            base = "Column"
        count = seen.get(base, 0) + 1
        seen[base] = count
        deduped.append(base if count == 1 else f"{base} ({count})")
    return deduped


def _normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')
    return df


def _promote_first_row_to_header(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    first_row = df.iloc[0].tolist()
    if not any(isinstance(val, str) and val.strip() for val in first_row):
        return df
    df = df[1:].reset_index(drop=True)
    headers = []
    for idx, val in enumerate(first_row):
        header = str(val).strip() if val not in (None, "") and str(val).strip() else f"Column {idx + 1}"
        headers.append(header)
    df.columns = _dedupe_columns(headers)
    return df


def _convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns that should be numeric to numeric type"""
    amount_keywords = ['amount', 'value', 'total', 'price', 'sum', 'income', 'expense', 'cost']
    
    for col in df.columns:
        col_lower = str(col).lower()
        # If column name suggests it should be numeric
        if any(keyword in col_lower for keyword in amount_keywords):
            # Try to convert to numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def load_excel_dataframe(file_path: str) -> pd.DataFrame:
    """Load Excel file and normalize into a usable table."""
    # Try reading with default settings first
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
    except Exception:
        # Fallback: try without specifying engine
        df = pd.read_excel(file_path)

    df = _normalize_dataframe(df)

    # If empty or all rows are empty, try reading without header
    if df.empty or df.dropna(axis=0, how='all').empty:
        try:
            df = pd.read_excel(file_path, engine="openpyxl", header=None)
        except Exception:
            df = pd.read_excel(file_path, header=None)
        df = _normalize_dataframe(df)

    if df.empty:
        return df

    # Check if columns are unnamed or numeric, and promote first row to header if needed
    unnamed_or_numeric = all(
        isinstance(col, int) or str(col).startswith("Unnamed")
        for col in df.columns
    )
    if unnamed_or_numeric:
        df = _promote_first_row_to_header(df)

    # Convert numeric columns
    df = _convert_numeric_columns(df)

    return df


@app.get("/")
async def root():
    return {"message": "CellSense API is running", "version": "1.0.0"}


@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    custom_keywords: Optional[str] = None
):
    """Upload and process an Excel file with optional custom keywords"""
    try:
        # Parse custom keywords if provided
        keywords_list = []
        if custom_keywords:
            try:
                keywords_list = json.loads(custom_keywords)
            except:
                keywords_list = [k.strip() for k in custom_keywords.split(',') if k.strip()]
        # Validate file type
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are supported")

        # Save file with a safe, non-user-controlled filename
        extension = os.path.splitext(file.filename)[1].lower()
        safe_filename = f"{uuid.uuid4().hex}{extension}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Read Excel file
        df = load_excel_dataframe(file_path)

        # Convert DataFrame to JSON-serializable format
        data = df.replace({np.nan: None}).to_dict(orient='records')
        columns = df.columns.tolist()

        # Perform basic analysis with custom keywords
        analysis = analyze_data(df, keywords_list)

        # Store data
        data_id = str(datetime.now().timestamp())
        data_store[data_id] = {
            'filename': file.filename,
            'stored_filename': safe_filename,
            'data': data,
            'columns': columns,
            'analysis': analysis,
            'custom_keywords': keywords_list
        }

        return {
            "message": "File uploaded successfully",
            "data_id": data_id,
            "filename": file.filename,
            "columns": columns,
            "row_count": len(data),
            "data": data,
            "analysis": analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.get("/api/data/{data_id}")
async def get_data(data_id: str):
    """Retrieve uploaded data by ID"""
    if data_id not in data_store:
        raise HTTPException(status_code=404, detail="Data not found")

    return data_store[data_id]


@app.post("/api/analyze")
async def analyze_uploaded_data(request: Dict[str, Any]):
    """Perform detailed analysis on uploaded data"""
    try:
        data_id = request.get('data_id')

        if data_id not in data_store:
            raise HTTPException(status_code=404, detail="Data not found")

        stored_data = data_store[data_id]
        df = pd.DataFrame(stored_data['data'])

        # Perform comprehensive analysis
        analysis = {
            'summary': analyze_data(df),
            'trends': calculate_trends(df),
            'categories': categorize_expenses(df)
        }

        return analysis

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing data: {str(e)}")


@app.post("/api/ask-ai")
async def ask_ai_question(request: AIQuestionRequest):
    """Answer questions about financial data using AI"""
    try:
        data_id = request.data_id
        question = request.question

        if data_id not in data_store:
            raise HTTPException(status_code=404, detail="Data not found")

        stored_data = data_store[data_id]
        df = pd.DataFrame(stored_data['data'])

        # Prepare context from the data
        analysis = stored_data.get('analysis', {})
        financial_summary = analysis.get('financial_summary', {})

        # Create a summary of the data for the AI
        context = f"""
Financial Data Summary:
- Total Records: {len(df)}
- Total Income: ${financial_summary.get('total_income', 0):,.2f}
- Total Expenses: ${financial_summary.get('total_expenses', 0):,.2f}
- Net Balance: ${financial_summary.get('net_balance', 0):,.2f}
- Detected Keywords: {', '.join(analysis.get('detected_keywords', [])[:10])}

Categories: {', '.join([cat['name'] for cat in financial_summary.get('categories', [])[:10]])}

User Question: {question}

Please provide a helpful, concise answer based on this financial data.
"""

        # Use a free AI API (Hugging Face or fallback to rule-based)
        try:
            # Try Hugging Face Inference API (free tier)
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api-inference.huggingface.co/models/google/flan-t5-large",
                    headers={"Content-Type": "application/json"},
                    json={"inputs": context}
                )

                if response.status_code == 200:
                    result = response.json()
                    ai_response = result[0]['generated_text'] if isinstance(result, list) else result.get('generated_text', '')

                    return {
                        "question": question,
                        "answer": ai_response,
                        "source": "AI (Hugging Face)"
                    }
        except Exception as ai_error:
            print(f"AI API error: {ai_error}")

        # Fallback to rule-based responses
        answer = generate_rule_based_answer(question, df, analysis)

        return {
            "question": question,
            "answer": answer,
            "source": "Rule-based analysis"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


def generate_rule_based_answer(question: str, df: pd.DataFrame, analysis: Dict[str, Any]) -> str:
    """Generate answers using rule-based logic"""
    question_lower = question.lower()
    financial_summary = analysis.get('financial_summary', {})

    # Income-related questions
    if any(word in question_lower for word in ['income', 'earn', 'revenue', 'salary']):
        total_income = financial_summary.get('total_income', 0)
        return f"Your total income is ${total_income:,.2f}. This includes all revenue, salary, and other income sources in your data."

    # Expense-related questions
    if any(word in question_lower for word in ['expense', 'spend', 'cost', 'payment']):
        total_expenses = financial_summary.get('total_expenses', 0)
        categories = financial_summary.get('categories', [])
        top_categories = ', '.join([cat['name'] for cat in categories[:3]])
        return f"Your total expenses are ${total_expenses:,.2f}. Top spending categories: {top_categories}."

    # Savings/Balance questions
    if any(word in question_lower for word in ['save', 'saving', 'balance', 'left', 'remaining']):
        net_balance = financial_summary.get('net_balance', 0)
        status = "positive" if net_balance >= 0 else "negative"
        return f"Your net balance is ${net_balance:,.2f} ({status}). This is the difference between your income and expenses."

    # Category questions
    if any(word in question_lower for word in ['category', 'categories', 'type', 'breakdown']):
        categories = financial_summary.get('categories', [])
        if categories:
            cat_list = ', '.join([f"{cat['name']} ({cat['count']} transactions)" for cat in categories[:5]])
            return f"Your transactions are categorized as: {cat_list}."
        return "No category information found in your data."

    # Summary/Overview questions
    if any(word in question_lower for word in ['summary', 'overview', 'total', 'how much']):
        return f"Financial Overview: Income: ${financial_summary.get('total_income', 0):,.2f}, Expenses: ${financial_summary.get('total_expenses', 0):,.2f}, Net: ${financial_summary.get('net_balance', 0):,.2f}. You have {analysis.get('total_rows', 0)} transactions recorded."

    # Keyword detection questions
    if any(word in question_lower for word in ['keyword', 'detect', 'found', 'type']):
        keywords = analysis.get('detected_keywords', [])
        if keywords:
            return f"Detected financial keywords in your data: {', '.join(keywords[:15])}."
        return "No specific financial keywords detected in your data."

    # Default response
    return f"Based on your data: You have {analysis.get('total_rows', 0)} transactions with a net balance of ${financial_summary.get('net_balance', 0):,.2f}. Try asking about income, expenses, categories, or savings for more specific insights."


def analyze_data(df: pd.DataFrame, custom_keywords: List[str] = None) -> Dict[str, Any]:
    """Analyze financial data and return statistics"""
    analysis = {
        'total_rows': len(df),
        'columns': df.columns.tolist(),
        'numeric_columns': [],
        'detected_keywords': []
    }

    # Combine default and custom keywords
    all_keywords = FINANCIAL_KEYWORDS.copy()
    if custom_keywords:
        all_keywords.extend([kw.lower() for kw in custom_keywords])

    # Detect which keywords are present in the data
    detected = set()
    for col in df.columns:
        col_lower = str(col).lower()
        for keyword in all_keywords:
            if keyword in col_lower:
                detected.add(keyword)

        # Check cell values too
        if df[col].dtype == 'object':
            for val in df[col].dropna().unique()[:100]:  # Check first 100 unique values
                val_lower = str(val).lower()
                for keyword in all_keywords:
                    if keyword in val_lower:
                        detected.add(keyword)

    analysis['detected_keywords'] = sorted(list(detected))

    # Analyze numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    for col in numeric_cols:
        col_stats = {
            'column': col,
            'sum': float(df[col].sum()) if not pd.isna(df[col].sum()) else 0,
            'mean': float(df[col].mean()) if not pd.isna(df[col].mean()) else 0,
            'min': float(df[col].min()) if not pd.isna(df[col].min()) else 0,
            'max': float(df[col].max()) if not pd.isna(df[col].max()) else 0,
            'std': float(df[col].std()) if not pd.isna(df[col].std()) else 0
        }
        analysis['numeric_columns'].append(col_stats)

    # Try to identify common financial columns
    analysis['financial_summary'] = identify_financial_data(df)

    return analysis


def identify_financial_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Identify and summarize financial data from the DataFrame"""
    summary = {
        'total_income': 0,
        'total_expenses': 0,
        'net_balance': 0,
        'categories': []
    }

    if df.empty:
        return summary

    # Look for common column names - expanded with more financial terms
    income_keywords = ['income', 'revenue', 'credit', 'earning', 'salary', 'bonus',
                      'dividend', 'interest', 'profit']
    expense_keywords = ['expense', 'cost', 'debit', 'spending', 'payment', 'emi',
                       'loan', 'liability', 'loss', 'premium']
    amount_keywords = ['amount', 'value', 'total', 'price', 'sum']
    type_keywords = ['type', 'transaction_type', 'category_type', 'transaction']
    category_keywords = ['category', 'description', 'name', 'asset', 'fund']

    income_col = None
    expense_col = None
    amount_col = None
    type_col = None
    category_col = None

    # First pass: identify columns by name
    for col in df.columns:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in income_keywords):
            income_col = col
        elif any(keyword in col_lower for keyword in expense_keywords):
            expense_col = col
        elif any(keyword in col_lower for keyword in amount_keywords):
            amount_col = col
        elif any(keyword in col_lower for keyword in type_keywords):
            type_col = col
        elif any(keyword in col_lower for keyword in category_keywords):
            category_col = col

    # Debug: Print detected columns
    print(f"DEBUG: Columns detected - amount_col: {amount_col}, type_col: {type_col}, income_col: {income_col}, expense_col: {expense_col}")
    print(f"DEBUG: DataFrame columns: {list(df.columns)}")
    print(f"DEBUG: DataFrame dtypes:\n{df.dtypes}")

    # If we have an Amount column and a Type column, use them to separate income/expenses
    if amount_col and type_col:
        print(f"DEBUG: Found Amount and Type columns")
        
        # Try to convert Amount column to numeric if it's not already
        if amount_col not in df.select_dtypes(include=[np.number]).columns.tolist():
            print(f"DEBUG: Converting {amount_col} to numeric")
            df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce')
        
        # Convert Type column to string for comparison
        df_type_str = df[type_col].astype(str).str.lower().str.strip()
        print(f"DEBUG: Unique Type values: {df_type_str.unique()}")
        
        # Sum amounts where Type indicates Income
        income_mask = df_type_str.isin(['income', 'credit', 'revenue', 'earning'])
        income_sum = df.loc[income_mask, amount_col].sum()
        if pd.notna(income_sum):
            summary['total_income'] = float(income_sum)
        print(f"DEBUG: Income mask matches: {income_mask.sum()}, total_income: {summary['total_income']}")
        
        # Sum amounts where Type indicates Expense
        expense_mask = df_type_str.isin(['expense', 'debit', 'spending', 'payment', 'cost'])
        expense_sum = df.loc[expense_mask, amount_col].sum()
        if pd.notna(expense_sum):
            summary['total_expenses'] = float(expense_sum)
        print(f"DEBUG: Expense mask matches: {expense_mask.sum()}, total_expenses: {summary['total_expenses']}")
        
        # If no matches found with exact terms, try pattern matching
        if summary['total_income'] == 0 and summary['total_expenses'] == 0:
            print("DEBUG: Trying pattern matching for Type column")
            income_mask = df_type_str.str.contains('income|credit|revenue|earning', case=False, na=False, regex=True)
            income_sum = df.loc[income_mask, amount_col].sum()
            if pd.notna(income_sum):
                summary['total_income'] = float(income_sum)
            
            expense_mask = df_type_str.str.contains('expense|debit|spending|payment|cost', case=False, na=False, regex=True)
            expense_sum = df.loc[expense_mask, amount_col].sum()
            if pd.notna(expense_sum):
                summary['total_expenses'] = float(expense_sum)
            print(f"DEBUG: After pattern matching - total_income: {summary['total_income']}, total_expenses: {summary['total_expenses']}")
    
    # Fallback: Calculate totals from separate income/expense columns
    if summary['total_income'] == 0 and summary['total_expenses'] == 0:
        print("DEBUG: Trying separate income/expense columns")
        if income_col and income_col in df.select_dtypes(include=[np.number]).columns:
            summary['total_income'] = float(df[income_col].sum())

        if expense_col and expense_col in df.select_dtypes(include=[np.number]).columns:
            summary['total_expenses'] = float(df[expense_col].sum())

    # If still no income/expenses found, try to infer from all numeric columns
    if summary['total_income'] == 0 and summary['total_expenses'] == 0:
        print("DEBUG: Trying to infer from numeric columns")
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        print(f"DEBUG: Numeric columns found: {numeric_cols}")
        if numeric_cols and type_col:
            df_type_str = df[type_col].astype(str).str.lower().str.strip()
            amount_col_to_use = numeric_cols[0]
            print(f"DEBUG: Using {amount_col_to_use} as amount column")
            
            income_mask = df_type_str.str.contains('income|credit|revenue|earning', case=False, na=False, regex=True)
            income_sum = df.loc[income_mask, amount_col_to_use].sum()
            if pd.notna(income_sum):
                summary['total_income'] = float(income_sum)
            
            expense_mask = df_type_str.str.contains('expense|debit|spending|payment|cost', case=False, na=False, regex=True)
            expense_sum = df.loc[expense_mask, amount_col_to_use].sum()
            if pd.notna(expense_sum):
                summary['total_expenses'] = float(expense_sum)
            print(f"DEBUG: Final - total_income: {summary['total_income']}, total_expenses: {summary['total_expenses']}")

    summary['net_balance'] = summary['total_income'] - summary['total_expenses']

    # Get categories if available
    if category_col and category_col in df.columns:
        categories = df[category_col].value_counts().to_dict()
        summary['categories'] = [{'name': str(k), 'count': int(v)} for k, v in categories.items()]

    print(f"DEBUG: Final summary: {summary}")
    return summary


def calculate_trends(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate trends from the data"""
    trends = {
        'by_month': [],
        'by_category': []
    }

    # Look for date column
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    if not date_cols:
        # Try to find date-like columns
        for col in df.columns:
            if 'date' in str(col).lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_cols.append(col)
                    break
                except:
                    pass

    if date_cols:
        date_col = date_cols[0]
        df['month'] = pd.to_datetime(df[date_col]).dt.to_period('M')

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            monthly = df.groupby('month')[numeric_cols[0]].sum()
            trends['by_month'] = [
                {'month': str(idx), 'value': float(val)}
                for idx, val in monthly.items()
            ]

    return trends


def categorize_expenses(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Categorize expenses from the data"""
    categories = []

    # Look for category column
    for col in df.columns:
        if 'category' in str(col).lower():
            # Look for amount column
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                amount_col = numeric_cols[0]
                grouped = df.groupby(col)[amount_col].sum()
                categories = [
                    {'category': str(idx), 'amount': float(val)}
                    for idx, val in grouped.items()
                ]
                break

    return categories


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
