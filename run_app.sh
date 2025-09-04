#!/bin/bash

echo "🚀 Starting Excel-to-SQL Reconciler..."
echo "📊 Project: AI-powered GL reconciliation tool"
echo "⏱️  Reduces month-end close from 6 hours to 30 seconds"
echo ""

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python -c "import streamlit, pandas, openai" 2>/dev/null || {
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
}

echo "✅ Dependencies ready!"
echo ""

# Check if data files exist
if [ ! -f "src/data/gl_excel.csv" ] || [ ! -f "src/data/gl_sql.csv" ]; then
    echo "📁 Generating sample data..."
    python generate_data.py
    echo "✅ Sample data generated!"
    echo ""
fi

# Display project stats
echo "📈 Project Statistics:"
echo "   Excel Rows: $(tail -n +2 src/data/gl_excel.csv | wc -l)"
echo "   SQL Rows: $(tail -n +2 src/data/gl_sql.csv | wc -l)"
echo "   Intentional Discrepancies: ~300"
echo ""

echo "🌐 Starting Streamlit server..."
echo "📱 App will be available at: http://localhost:8501"
echo ""
echo "💡 Pro Tip: Get your OpenAI API key from https://platform.openai.com"
echo ""

# Start the Streamlit app
python -m streamlit run src/app.py --server.port 8501
