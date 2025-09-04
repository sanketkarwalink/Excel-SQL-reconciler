import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_gl_data(num_rows=50000):
    """Generate general ledger data with realistic financial transactions"""
    
    # Account codes and names
    accounts = {
        1000: "Cash",
        1200: "Accounts Receivable", 
        1500: "Inventory",
        1700: "Prepaid Expenses",
        2000: "Accounts Payable",
        2100: "Accrued Liabilities",
        3000: "Revenue",
        4000: "Cost of Goods Sold",
        5000: "Salaries Expense",
        5100: "Rent Expense",
        5200: "Utilities Expense",
        6000: "Marketing Expense"
    }
    
    # Generate data
    data = []
    start_date = datetime(2024, 1, 1)
    
    for i in range(1, num_rows + 1):
        # Random date within 2024
        random_days = random.randint(0, 364)
        transaction_date = start_date + timedelta(days=random_days)
        
        # Random account
        account_code = random.choice(list(accounts.keys()))
        account_name = accounts[account_code]
        
        # Generate debit/credit amounts (one will be 0)
        amount = round(random.uniform(10.00, 50000.00), 2)
        
        # Randomly assign to debit or credit
        if random.choice([True, False]):
            debit = amount
            credit = 0.00
        else:
            debit = 0.00
            credit = amount
            
        # Generate description and reference
        descriptions = [
            "Monthly Invoice", "Customer Payment", "Supplier Payment", 
            "Salary Payment", "Rent Payment", "Utility Bill",
            "Sales Transaction", "Purchase Order", "Bank Transfer",
            "Adjustment Entry", "Depreciation", "Interest Payment"
        ]
        
        description = random.choice(descriptions)
        reference = f"REF{i:06d}"
        
        data.append({
            'transaction_id': i,
            'date': transaction_date.strftime('%Y-%m-%d'),
            'account_code': account_code,
            'account_name': account_name,
            'debit': debit,
            'credit': credit,
            'description': description,
            'reference': reference
        })
    
    return pd.DataFrame(data)

def create_sql_version_with_discrepancies(df_excel):
    """Create SQL version with intentional discrepancies"""
    df_sql = df_excel.copy()
    
    # Introduce 300 intentional differences
    num_discrepancies = 300
    discrepancy_indices = random.sample(range(len(df_sql)), num_discrepancies)
    
    for idx in discrepancy_indices:
        discrepancy_type = random.choice([
            'amount_difference', 'date_format', 'missing_row', 
            'rounding_difference', 'account_mismatch'
        ])
        
        if discrepancy_type == 'amount_difference':
            # Change debit/credit amounts
            if df_sql.iloc[idx]['debit'] > 0:
                df_sql.iloc[idx, df_sql.columns.get_loc('debit')] += random.uniform(-100, 100)
            else:
                df_sql.iloc[idx, df_sql.columns.get_loc('credit')] += random.uniform(-100, 100)
                
        elif discrepancy_type == 'date_format':
            # Change date format slightly
            original_date = datetime.strptime(df_sql.iloc[idx]['date'], '%Y-%m-%d')
            new_date = original_date + timedelta(days=random.choice([-1, 1]))
            df_sql.iloc[idx, df_sql.columns.get_loc('date')] = new_date.strftime('%Y-%m-%d')
            
        elif discrepancy_type == 'rounding_difference':
            # Small rounding differences
            if df_sql.iloc[idx]['debit'] > 0:
                df_sql.iloc[idx, df_sql.columns.get_loc('debit')] = round(df_sql.iloc[idx]['debit'] + 0.01, 2)
            else:
                df_sql.iloc[idx, df_sql.columns.get_loc('credit')] = round(df_sql.iloc[idx]['credit'] + 0.01, 2)
                
        elif discrepancy_type == 'account_mismatch':
            # Change account code
            accounts = [1000, 1200, 1500, 2000, 2100, 3000, 4000, 5000]
            new_account = random.choice(accounts)
            df_sql.iloc[idx, df_sql.columns.get_loc('account_code')] = new_account
            
    # Remove some rows to simulate missing data (50 rows)
    rows_to_remove = random.sample(range(len(df_sql)), 50)
    df_sql = df_sql.drop(rows_to_remove).reset_index(drop=True)
    
    return df_sql

if __name__ == "__main__":
    print("Generating Excel GL data (50k rows)...")
    df_excel = generate_gl_data(50000)
    
    print("Creating SQL version with discrepancies...")
    df_sql = create_sql_version_with_discrepancies(df_excel)
    
    print("Saving files...")
    df_excel.to_csv('src/data/gl_excel.csv', index=False)
    df_sql.to_csv('src/data/gl_sql.csv', index=False)
    
    print(f"Excel file: {len(df_excel)} rows")
    print(f"SQL file: {len(df_sql)} rows")
    print("Data generation complete!")
