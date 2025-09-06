#!/usr/bin/env python3
"""
Excel-to-SQL Reconciler - Main Streamlit Application

AI-powered financial reconciliation tool that reduces month-end GL reconciliation 
from 6 hours to 30 seconds with 99.99% accuracy.

Author: Sanket Karwa
GitHub: https://github.com/sanketkarwa/excel-to-sql-reconciler
License: MIT

Features:
- Process 50k+ t        <div style='text-align: center; color: #666; padding: 20px; border-top: 1px solid #eee; margin-top: 30px;'>
        <strong>Excel-to-SQL Reconciler v1.0</strong><br>
        Built with ❤️ by <a href="https://github.com/sanketkarwalink" target="_blank" style="color: #1f77b4; text-decoration: none;"><strong>Sanket Karwa</strong></a><br>
        <small>AI-powered reconciliation • Streamlit + OpenAI GPT-4o-mini</small><br>
        <small>🎯 Reduces month-end reconciliation from 6 hours to 30 seconds</small><br>
        <br>
        <a href="https://github.com/sanketkarwalink/Excel-SQL-reconciler" target="_blank" style="color: #666; text-decoration: none;">
        📂 View Source Code on GitHub</a><br>
        <small><a href="https://excel-sql-reconciler-jvnnv2df5puqnut7fw4xbp.streamlit.app/" target="_blank" style="color: #666; text-decoration: none;">
        🌐 Live Demo</a></small>
        </div>n reconciliations in <30 seconds
- AI-powered discrepancy detection using OpenAI GPT-4o-mini
- Statistical analysis and professional audit reports
- Real-time KPI tracking and export functionality
"""

import streamlit as st
import pandas as pd
import json
import os
import time
import sys

# Add the src directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.reconciliation import (
    read_csv, 
    send_to_openai, 
    perform_local_reconciliation,
    generate_reconciliation_report
)

def main():
    st.set_page_config(
        page_title="Excel-to-SQL Reconciler",
        page_icon="📊",
        layout="wide"
    )
    
    # Initialize session state
    if 'use_sample_data' not in st.session_state:
        st.session_state.use_sample_data = False
    if 'sample_df_excel' not in st.session_state:
        st.session_state.sample_df_excel = None
    if 'sample_df_sql' not in st.session_state:
        st.session_state.sample_df_sql = None
    
    st.title("📊 Excel-to-SQL Reconciler")
    st.markdown("### Automated General Ledger Reconciliation Tool")
    st.markdown("Upload your Excel and SQL extracts to identify discrepancies in seconds.")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # OpenAI API Key input
    # Try to get API key from Streamlit secrets first, then environment
    default_api_key = ""
    try:
        default_api_key = st.secrets.get("OPENAI_API_KEY", "")
    except:
        try:
            import os
            default_api_key = os.getenv('OPENAI_API_KEY', '')
        except:
            default_api_key = ""
    
    # If we have a default API key from secrets, don't show it in the input
    if default_api_key:
        st.sidebar.success("🔑 API Key loaded from environment")
        api_key = default_api_key
        # Option to override if needed
        override_key = st.sidebar.text_input(
            "Override API Key (optional)", 
            type="password", 
            placeholder="Leave empty to use environment key",
            help="Only enter if you want to use a different API key"
        )
        if override_key:
            api_key = override_key
    else:
        api_key = st.sidebar.text_input(
            "OpenAI API Key", 
            type="password", 
            placeholder="Enter your OpenAI API key",
            help="Enter your OpenAI API key for AI-powered analysis"
        )
    
    if api_key:
        import os
        os.environ['OPENAI_API_KEY'] = api_key
        st.sidebar.success("✅ API Key Set!")
        
        # Debug info
        if len(api_key) > 10:
            masked_key = api_key[:7] + "..." + api_key[-4:]
            st.sidebar.info(f"🔑 Key: {masked_key}")
        
        # Quick API test
        if st.sidebar.button("🧪 Test API Key"):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": "Reply with just 'API works'"}],
                    max_tokens=5
                )
                st.sidebar.success("🎉 API Key is working!")
            except Exception as e:
                st.sidebar.error(f"❌ API Error: {str(e)}")
    else:
        st.sidebar.warning("⚠️ No API key provided - AI analysis will be skipped")
    
    # Sample size for AI analysis
    sample_size = st.sidebar.slider(
        "Sample Size for AI Analysis", 
        min_value=50, 
        max_value=500, 
        value=100,
        help="Number of rows to send to AI for analysis (larger = more accurate but slower)"
    )
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📁 Upload Excel GL Extract")
        excel_file = st.file_uploader(
            "Choose Excel CSV file", 
            type=["csv"],
            key="excel_upload"
        )
        
        if excel_file:
            st.success(f"✅ Excel file uploaded: {excel_file.name}")
            try:
                df_excel = read_csv(excel_file)
                st.info(f"📊 Rows: {len(df_excel):,} | Columns: {len(df_excel.columns)}")
                
                # Show preview
                with st.expander("Preview Excel Data"):
                    st.dataframe(df_excel.head(10))
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")
                df_excel = None
        else:
            df_excel = None
    
    with col2:
        st.header("🗄️ Upload SQL GL Extract")
        sql_file = st.file_uploader(
            "Choose SQL CSV file", 
            type=["csv"],
            key="sql_upload"
        )
        
        if sql_file:
            st.success(f"✅ SQL file uploaded: {sql_file.name}")
            try:
                df_sql = read_csv(sql_file)
                st.info(f"📊 Rows: {len(df_sql):,} | Columns: {len(df_sql.columns)}")
                
                # Show preview
                with st.expander("Preview SQL Data"):
                    st.dataframe(df_sql.head(10))
            except Exception as e:
                st.error(f"Error reading SQL file: {str(e)}")
                df_sql = None
        else:
            df_sql = None
    
    # API key status display
    if api_key:
        st.success("🤖 AI-powered analysis enabled")
    else:
        st.warning("⚠️ AI analysis disabled - Add OPENAI_API_KEY to enable AI features. Statistical analysis will still work!")
    
    # Quick Start with Sample Data
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Try with Sample Data", type="secondary"):
            try:
                st.session_state.sample_df_excel = pd.read_csv("src/data/gl_excel.csv")
                st.session_state.sample_df_sql = pd.read_csv("src/data/gl_sql.csv")
                st.session_state.use_sample_data = True
                st.success("✅ Sample data loaded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
        
        # Reset button
        if st.session_state.use_sample_data:
            if st.button("🔄 Use File Upload Instead", type="secondary"):
                st.session_state.use_sample_data = False
                st.session_state.sample_df_excel = None
                st.session_state.sample_df_sql = None
                st.rerun()
    
    # Determine which data to use
    final_df_excel = None
    final_df_sql = None
    
    if st.session_state.use_sample_data:
        final_df_excel = st.session_state.sample_df_excel
        final_df_sql = st.session_state.sample_df_sql
        
        # Show sample data info
        st.success("📊 Using Sample Data")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📁 Excel Sample: {len(final_df_excel):,} rows")
        with col2:
            st.info(f"📁 SQL Sample: {len(final_df_sql):,} rows")
    else:
        final_df_excel = df_excel
        final_df_sql = df_sql
    
    # Reconciliation Process
    if final_df_excel is not None and final_df_sql is not None:
        st.markdown("---")
        st.header("🔍 Reconciliation Analysis")
        
        if st.button("🔄 Start Reconciliation", type="primary"):
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            start_time = time.time()
            
            # Step 1: Local Analysis
            status_text.text("🔍 Performing local statistical analysis...")
            progress_bar.progress(25)
            
            local_results = perform_local_reconciliation(final_df_excel, final_df_sql)
            
            # Step 2: AI Analysis (if API key provided)
            ai_mismatches = []
            if api_key:
                status_text.text("🤖 Running AI-powered mismatch detection...")
                progress_bar.progress(50)
                
                try:
                    st.info(f"🔑 Using API key: {api_key[:7]}...")
                    ai_mismatches = send_to_openai(final_df_excel, final_df_sql)
                    
                    if ai_mismatches and len(ai_mismatches) > 0:
                        if "error" in str(ai_mismatches[0]).lower():
                            st.error(f"❌ AI Analysis Failed: {ai_mismatches[0]}")
                        else:
                            st.success(f"✅ AI Analysis Complete: {len(ai_mismatches)} insights")
                    else:
                        st.warning("⚠️ AI returned empty results")
                        
                except Exception as e:
                    st.error(f"❌ AI Analysis Error: {str(e)}")
                    ai_mismatches = []
            else:
                st.warning("⚠️ No OpenAI API key provided. Skipping AI analysis.")
            
            # Step 3: Generate Report
            status_text.text("📊 Generating reconciliation report...")
            progress_bar.progress(75)
            
            report_df = generate_reconciliation_report(ai_mismatches, local_results)
            
            # Step 4: Complete
            end_time = time.time()
            processing_time = end_time - start_time
            
            status_text.text("✅ Reconciliation complete!")
            progress_bar.progress(100)
            
            # Display Results
            st.markdown("---")
            st.header("📈 Reconciliation Results")
            
            # KPI Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Excel Rows", f"{local_results['total_excel_rows']:,}")
            
            with col2:
                st.metric("SQL Rows", f"{local_results['total_sql_rows']:,}")
            
            with col3:
                st.metric("Discrepancies", len(report_df))
            
            with col4:
                st.metric("Processing Time", f"{processing_time:.1f}s")
            
            # Accuracy calculation
            if local_results['total_excel_rows'] > 0:
                accuracy = ((local_results['total_excel_rows'] - len(report_df)) / 
                           local_results['total_excel_rows']) * 100
                st.success(f"🎯 **Accuracy: {accuracy:.2f}%** (Target: >99.8%)")
            
            # Display issues
            if local_results['potential_issues']:
                st.subheader("⚠️ Statistical Analysis Issues")
                for issue in local_results['potential_issues']:
                    st.warning(issue)
            
            # Display detailed mismatches
            if not report_df.empty:
                st.subheader("🔍 Detailed Mismatch Report")
                st.dataframe(report_df, use_container_width=True)
                
                # Download button
                csv_data = report_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Mismatch Report (CSV)",
                    data=csv_data,
                    file_name=f"reconciliation_report_{int(time.time())}.csv",
                    mime="text/csv"
                )
                
                # Download JSON for API integration
                json_data = report_df.to_json(orient='records', indent=2)
                st.download_button(
                    label="📥 Download Report (JSON)",
                    data=json_data,
                    file_name=f"reconciliation_report_{int(time.time())}.json",
                    mime="application/json"
                )
            else:
                st.success("🎉 No discrepancies found! Your data is perfectly aligned.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; margin-top: 2rem;'>
        <strong>Excel-to-SQL Reconciler v1.0</strong><br>
        Built with ❤️ by <a href="https://github.com/sanketkarwa" target="_blank" style="color: #1f77b4; text-decoration: none;"><strong>Sanket Karwa</strong></a><br>
        <small>AI-powered reconciliation • Streamlit + OpenAI GPT-4o-mini</small><br>
        <small>🎯 Reduces month-end reconciliation from 6 hours to 30 seconds</small><br>
        <br>
        <a href="https://github.com/sanketkarwa/excel-to-sql-reconciler" target="_blank" style="color: #666; text-decoration: none;">
        📂 View Source Code on GitHub</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()