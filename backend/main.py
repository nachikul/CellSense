from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import os
import json
from datetime import datetime

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


@app.get("/")
async def root():
    return {"message": "CellSense API is running", "version": "1.0.0"}


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process an Excel file"""
    try:
        # Validate file type
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are supported")
        
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Convert DataFrame to JSON-serializable format
        data = df.replace({np.nan: None}).to_dict(orient='records')
        columns = df.columns.tolist()
        
        # Perform basic analysis
        analysis = analyze_data(df)
        
        # Store data
        data_id = str(datetime.now().timestamp())
        data_store[data_id] = {
            'filename': file.filename,
            'data': data,
            'columns': columns,
            'analysis': analysis
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


def analyze_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze financial data and return statistics"""
    analysis = {
        'total_rows': len(df),
        'columns': df.columns.tolist(),
        'numeric_columns': []
    }
    
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
    
    # Look for common column names
    income_keywords = ['income', 'revenue', 'credit', 'earning']
    expense_keywords = ['expense', 'cost', 'debit', 'spending', 'payment']
    category_keywords = ['category', 'type', 'description', 'name']
    
    income_col = None
    expense_col = None
    category_col = None
    
    for col in df.columns:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in income_keywords):
            income_col = col
        elif any(keyword in col_lower for keyword in expense_keywords):
            expense_col = col
        elif any(keyword in col_lower for keyword in category_keywords):
            category_col = col
    
    # Calculate totals
    if income_col and income_col in df.select_dtypes(include=[np.number]).columns:
        summary['total_income'] = float(df[income_col].sum())
    
    if expense_col and expense_col in df.select_dtypes(include=[np.number]).columns:
        summary['total_expenses'] = float(df[expense_col].sum())
    
    summary['net_balance'] = summary['total_income'] - summary['total_expenses']
    
    # Get categories if available
    if category_col and category_col in df.columns:
        categories = df[category_col].value_counts().to_dict()
        summary['categories'] = [{'name': str(k), 'count': int(v)} for k, v in categories.items()]
    
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
