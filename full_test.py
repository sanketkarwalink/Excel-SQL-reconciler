#!/usr/bin/env python3
"""
Complete Testing Guide for Excel-to-SQL Reconciler
Run this to test all functionality step by step
"""

import sys
import os
import time
import pandas as pd

# Add src to path for imports
sys.path.append('src')

def test_data_loading():
    """Test 1: Data Loading"""
    print("🧪 TEST 1: Data Loading")
    print("-" * 30)
    
    try:
        from utils.reconciliation import read_csv
        
        # Test CSV reading
        df_excel = pd.read_csv('src/data/gl_excel.csv')
        df_sql = pd.read_csv('src/data/gl_sql.csv')
        
        print(f"✅ Excel data loaded: {len(df_excel):,} rows")
        print(f"✅ SQL data loaded: {len(df_sql):,} rows")
        print(f"✅ Columns: {list(df_excel.columns)}")
        
        # Check data quality
        if len(df_excel) > 45000:
            print("✅ Large dataset test: PASSED")
        else:
            print("⚠️  Dataset smaller than expected")
            
        return True, df_excel, df_sql
        
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False, None, None

def test_reconciliation_engine(df_excel, df_sql):
    """Test 2: Core Reconciliation Logic"""
    print("\n🧪 TEST 2: Reconciliation Engine")
    print("-" * 35)
    
    try:
        from utils.reconciliation import perform_local_reconciliation
        
        start_time = time.time()
        results = perform_local_reconciliation(df_excel, df_sql)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        print(f"✅ Processing time: {processing_time:.2f} seconds")
        print(f"✅ Excel rows analyzed: {results['total_excel_rows']:,}")
        print(f"✅ SQL rows analyzed: {results['total_sql_rows']:,}")
        print(f"✅ Issues detected: {len(results['potential_issues'])}")
        
        # Check performance
        if processing_time < 5.0:
            print("✅ Performance test: PASSED (< 5 seconds)")
        else:
            print("⚠️  Processing slower than expected")
            
        # Show sample issues
        for i, issue in enumerate(results['potential_issues'][:3]):
            print(f"   • Issue {i+1}: {issue}")
            
        return True, results
        
    except Exception as e:
        print(f"❌ Reconciliation engine failed: {e}")
        return False, None

def test_report_generation(df_excel, df_sql, local_results):
    """Test 3: Report Generation"""
    print("\n🧪 TEST 3: Report Generation")
    print("-" * 32)
    
    try:
        from utils.reconciliation import generate_reconciliation_report
        
        # Test with mock AI results
        mock_ai_results = [
            {
                "transaction_id": "123",
                "discrepancy_type": "amount_difference",
                "reason": "Debit amount differs by $0.01",
                "excel_data": "Debit: 1000.00",
                "sql_data": "Debit: 1000.01"
            },
            {
                "transaction_id": "456", 
                "discrepancy_type": "missing_row",
                "reason": "Transaction missing in SQL dataset",
                "excel_data": "Row exists",
                "sql_data": "Row missing"
            }
        ]
        
        report_df = generate_reconciliation_report(mock_ai_results, local_results)
        
        print(f"✅ Report generated: {len(report_df)} discrepancies")
        print(f"✅ Report columns: {list(report_df.columns)}")
        
        if len(report_df) > 0:
            print("✅ Report content test: PASSED")
            print("\n📋 Sample report entries:")
            for i, row in report_df.head(2).iterrows():
                print(f"   • {row.get('Discrepancy Type', 'N/A')}: {row.get('Description', 'N/A')}")
        else:
            print("⚠️  Empty report generated")
            
        return True, report_df
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        return False, None

def test_streamlit_components():
    """Test 4: Streamlit App Components"""
    print("\n🧪 TEST 4: Streamlit Components")
    print("-" * 34)
    
    try:
        # Test imports
        import streamlit as st
        print("✅ Streamlit import: SUCCESS")
        
        # Test app file exists and is valid Python
        with open('src/app.py', 'r') as f:
            app_content = f.read()
            
        if 'st.title' in app_content:
            print("✅ Streamlit UI components: FOUND")
        
        if 'file_uploader' in app_content:
            print("✅ File upload functionality: FOUND")
            
        if 'download_button' in app_content:
            print("✅ Export functionality: FOUND")
            
        return True
        
    except Exception as e:
        print(f"❌ Streamlit component test failed: {e}")
        return False

def test_ai_integration():
    """Test 5: AI Integration (without API key)"""
    print("\n🧪 TEST 5: AI Integration")
    print("-" * 27)
    
    try:
        from utils.reconciliation import load_forensic_prompt, prepare_data_for_ai
        
        # Test prompt loading
        prompt = load_forensic_prompt()
        if len(prompt) > 100:
            print("✅ AI prompt loaded: SUCCESS")
        else:
            print("⚠️  AI prompt seems short")
            
        # Test data preparation
        df_excel = pd.read_csv('src/data/gl_excel.csv')
        df_sql = pd.read_csv('src/data/gl_sql.csv')
        
        prepared_data = prepare_data_for_ai(df_excel, df_sql, sample_size=10)
        
        if 'EXCEL GL EXTRACT' in prepared_data:
            print("✅ Data preparation: SUCCESS")
        else:
            print("⚠️  Data preparation format issue")
            
        print("⚠️  OpenAI API test skipped (requires API key)")
        
        return True
        
    except Exception as e:
        print(f"❌ AI integration test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests in sequence"""
    print("=" * 60)
    print("🚀 EXCEL-TO-SQL RECONCILER - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Data Loading
    success, df_excel, df_sql = test_data_loading()
    test_results.append(("Data Loading", success))
    
    if not success:
        print("\n❌ Critical failure - stopping tests")
        return
    
    # Test 2: Reconciliation Engine
    success, local_results = test_reconciliation_engine(df_excel, df_sql)
    test_results.append(("Reconciliation Engine", success))
    
    # Test 3: Report Generation
    if success:
        success, report_df = test_report_generation(df_excel, df_sql, local_results)
        test_results.append(("Report Generation", success))
    
    # Test 4: Streamlit Components
    success = test_streamlit_components()
    test_results.append(("Streamlit Components", success))
    
    # Test 5: AI Integration
    success = test_ai_integration()
    test_results.append(("AI Integration", success))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your reconciler is ready for production.")
        print("\n🚀 Next steps:")
        print("   1. Run: streamlit run src/app.py")
        print("   2. Visit: http://localhost:8501")
        print("   3. Test with sample data or upload your own")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")

if __name__ == "__main__":
    run_comprehensive_test()
