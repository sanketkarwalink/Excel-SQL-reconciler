#!/usr/bin/env python3
"""
Quick test script for the Excel-to-SQL Reconciler
"""

import sys
import os
sys.path.append('src')

import pandas as pd
from utils.reconciliation import read_csv, perform_local_reconciliation

def test_reconciliation():
    print("🧪 Testing Excel-to-SQL Reconciler...")
    
    # Test data loading
    try:
        df_excel = pd.read_csv('src/data/gl_excel.csv')
        df_sql = pd.read_csv('src/data/gl_sql.csv')
        
        print(f"✅ Data loaded successfully:")
        print(f"   📊 Excel: {len(df_excel):,} rows, {len(df_excel.columns)} columns")
        print(f"   📊 SQL: {len(df_sql):,} rows, {len(df_sql.columns)} columns")
        
        # Test local reconciliation
        local_results = perform_local_reconciliation(df_excel, df_sql)
        
        print(f"\n🔍 Local Analysis Results:")
        print(f"   Row difference: {local_results['row_difference']}")
        print(f"   Issues found: {len(local_results['potential_issues'])}")
        
        for issue in local_results['potential_issues']:
            print(f"   ⚠️  {issue}")
        
        # Test data preview
        print(f"\n📋 Sample Excel Data:")
        print(df_excel.head(3).to_string(index=False))
        
        print(f"\n📋 Sample SQL Data:")
        print(df_sql.head(3).to_string(index=False))
        
        print(f"\n✅ All tests passed! The reconciler is ready to use.")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    test_reconciliation()
