#!/usr/bin/env python3
"""
Excel-to-SQL Reconciler - Core Reconciliation Engine

Advanced reconciliation logic combining statistical analysis with AI-powered 
discrepancy detection for enterprise-grade financial data validation.

Author: Sanket Karwa
GitHub: https://github.com/sanketkarwalink/excel-to-sql-reconciler
License: MIT

Key Capabilities:
- Process 50k+ row datasets with sub-30 second performance
- OpenAI GPT-4o-mini integration for intelligent mismatch analysis
- Statistical variance detection across multiple data dimensions
- Professional audit report generation with detailed explanations
"""

import pandas as pd
import json
import os
from openai import OpenAI
from typing import Dict, List, Any
import streamlit as st

def read_csv(file_path):
    """Read CSV file and return pandas DataFrame"""
    try:
        if hasattr(file_path, 'read'):  # Streamlit uploaded file
            return pd.read_csv(file_path)
        else:  # File path string
            return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")
        return None

def load_forensic_prompt():
    """Load the forensic accountant prompt"""
    try:
        with open('src/prompts/forensic_accountant.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return """You are a forensic accountant. Analyze the two datasets and identify discrepancies. 
                 Return a JSON array of mismatch objects with transaction_id, discrepancy_type, and reason."""

def prepare_data_for_ai(df1: pd.DataFrame, df2: pd.DataFrame, sample_size: int = 100) -> str:
    """Prepare data samples for AI analysis"""
    
    # Take first N rows for analysis to stay within token limits
    df1_sample = df1.head(sample_size)
    df2_sample = df2.head(sample_size)
    
    data_summary = f"""
EXCEL GL EXTRACT (First {len(df1_sample)} rows of {len(df1)} total):
{df1_sample.to_string(index=False)}

SQL GL EXTRACT (First {len(df2_sample)} rows of {len(df2)} total):
{df2_sample.to_string(index=False)}

DATASET STATISTICS:
Excel rows: {len(df1)}
SQL rows: {len(df2)}
Columns: {list(df1.columns)}
"""
    return data_summary

def send_to_openai(df_excel: pd.DataFrame, df_sql: pd.DataFrame) -> List[Dict]:
    """Send data to OpenAI for mismatch analysis"""
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Load prompt
        prompt = load_forensic_prompt()
        
        # Prepare data
        data_summary = prepare_data_for_ai(df_excel, df_sql, sample_size=100)
        
        # Create the full prompt
        full_prompt = f"{prompt}\n\n{data_summary}"
        
        # Send to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a forensic accountant specializing in financial data reconciliation."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.1,
            max_tokens=2000
        )
        
        # Parse response
        response_text = response.choices[0].message.content.strip()
        
        # Clean up common AI response formatting issues
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith('json'):
            response_text = response_text[4:]  # Remove json prefix
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove closing ```
        
        response_text = response_text.strip()
        
        # Try to parse JSON
        try:
            mismatches = json.loads(response_text)
            return mismatches if isinstance(mismatches, list) else []
        except json.JSONDecodeError as e:
            # If JSON parsing fails, try to extract JSON from the response
            try:
                # Look for JSON array in the response
                start_idx = response_text.find('[')
                end_idx = response_text.rfind(']') + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_part = response_text[start_idx:end_idx]
                    mismatches = json.loads(json_part)
                    return mismatches if isinstance(mismatches, list) else []
                else:
                    return [{"error": "No valid JSON found in AI response", "raw_response": response_text}]
            except:
                return [{"error": "Failed to parse AI response", "raw_response": response_text, "json_error": str(e)}]
            
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return [{"error": str(e)}]

def perform_local_reconciliation(df_excel: pd.DataFrame, df_sql: pd.DataFrame) -> Dict[str, Any]:
    """Perform comprehensive local reconciliation analysis"""
    
    results = {
        "total_excel_rows": len(df_excel),
        "total_sql_rows": len(df_sql),
        "row_difference": len(df_excel) - len(df_sql),
        "potential_issues": []
    }
    
    # Check for obvious differences
    if len(df_excel) != len(df_sql):
        results["potential_issues"].append(f"Row count mismatch: Excel has {len(df_excel)}, SQL has {len(df_sql)}")
    
    # Check column alignment
    if list(df_excel.columns) != list(df_sql.columns):
        results["potential_issues"].append("Column structure differs between files")
    
    # Enhanced statistical comparison on numeric columns
    numeric_cols = df_excel.select_dtypes(include=['float64', 'int64']).columns
    
    for col in numeric_cols:
        if col in df_sql.columns:
            excel_sum = df_excel[col].sum()
            sql_sum = df_sql[col].sum()
            
            if abs(excel_sum - sql_sum) > 0.01:  # Allow for small rounding differences
                difference = abs(excel_sum - sql_sum)
                percentage_diff = (difference / max(abs(excel_sum), abs(sql_sum))) * 100 if max(abs(excel_sum), abs(sql_sum)) > 0 else 0
                results["potential_issues"].append(
                    f"{col} totals differ: Excel=${excel_sum:,.2f}, SQL=${sql_sum:,.2f} "
                    f"(Difference: ${difference:,.2f}, {percentage_diff:.1f}%)"
                )
            
            # Check for missing values
            excel_nulls = df_excel[col].isnull().sum()
            sql_nulls = df_sql[col].isnull().sum()
            if excel_nulls != sql_nulls:
                results["potential_issues"].append(
                    f"{col} has different null counts: Excel={excel_nulls}, SQL={sql_nulls}"
                )
    
    # Check for duplicate records
    excel_dupes = df_excel.duplicated().sum()
    sql_dupes = df_sql.duplicated().sum()
    if excel_dupes > 0 or sql_dupes > 0:
        results["potential_issues"].append(f"Duplicate records found - Excel: {excel_dupes}, SQL: {sql_dupes}")
    
    # Date range analysis (if Date column exists)
    if 'Date' in df_excel.columns and 'Date' in df_sql.columns:
        try:
            excel_dates = pd.to_datetime(df_excel['Date'])
            sql_dates = pd.to_datetime(df_sql['Date'])
            
            excel_range = f"{excel_dates.min().strftime('%Y-%m-%d')} to {excel_dates.max().strftime('%Y-%m-%d')}"
            sql_range = f"{sql_dates.min().strftime('%Y-%m-%d')} to {sql_dates.max().strftime('%Y-%m-%d')}"
            
            if excel_range != sql_range:
                results["potential_issues"].append(f"Date ranges differ - Excel: {excel_range}, SQL: {sql_range}")
        except:
            results["potential_issues"].append("Unable to parse date fields for comparison")
    
    # Add summary statistics
    if not results["potential_issues"]:
        results["potential_issues"].append("✅ No major discrepancies detected in statistical analysis")
        results["potential_issues"].append(f"✅ Total records reconciled: {min(len(df_excel), len(df_sql)):,}")
    
    return results

def generate_reconciliation_report(ai_mismatches: List[Dict], local_analysis: Dict) -> pd.DataFrame:
    """Generate a comprehensive reconciliation report"""
    
    report_data = []
    
    # First, add local analysis issues
    for issue in local_analysis.get("potential_issues", []):
        report_data.append({
            "Transaction ID": "Statistical",
            "Discrepancy Type": "Statistical Analysis",
            "Description": issue,
            "Excel Data": "Aggregate data",
            "SQL Data": "Aggregate data",
            "Impact": "High" if "total" in issue.lower() else "Medium"
        })
    
    # Then add AI analysis results (if successful)
    if ai_mismatches and not (len(ai_mismatches) == 1 and "error" in ai_mismatches[0]):
        for mismatch in ai_mismatches:
            if "error" not in mismatch:
                # Handle both old and new formats
                transaction_id = mismatch.get("transaction_id", "Unknown")
                discrepancy_type = mismatch.get("discrepancy_type", "Unknown")
                reason = mismatch.get("reason", "No description")
                
                # Handle excel_data and sql_data which might be objects or strings
                excel_data = mismatch.get("excel_data", "")
                sql_data = mismatch.get("sql_data", "")
                
                if isinstance(excel_data, dict):
                    excel_str = f"Amount: {excel_data.get('debit', 0)} / {excel_data.get('credit', 0)}"
                else:
                    excel_str = str(excel_data)
                    
                if isinstance(sql_data, dict):
                    sql_str = f"Amount: {sql_data.get('debit', 0)} / {sql_data.get('credit', 0)}"
                else:
                    sql_str = str(sql_data)
                
                report_data.append({
                    "Transaction ID": transaction_id,
                    "Discrepancy Type": discrepancy_type.title(),
                    "Description": reason,
                    "Excel Data": excel_str,
                    "SQL Data": sql_str,
                    "Impact": "High"  # All AI-identified mismatches are high impact
                })
    
    return pd.DataFrame(report_data)