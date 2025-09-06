# Excel-to-SQL Reconciler

AI-powered tool to compare Excel and SQL data files and find differences.

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the app:**
```bash
python src/app.py
```

3. **Open your browser:** Go to `http://localhost:8501`

## How to Use

1. Upload your Excel file (.csv format)
2. Upload your SQL data file (.csv format)  
3. Add your OpenAI API key in the `.env` file
4. Click "Start Reconciliation"
5. Download the results

## What It Does

- Compares data between two files
- Finds missing rows and differences
- Uses AI to analyze discrepancies
- Generates a report of mismatches

## Requirements

- Python 3.8+
- OpenAI API key
- CSV files to compare

## Setup

1. **Clone this repository**
2. **Create `.env` file:**
```
OPENAI_API_KEY=your-api-key-here
```
3. **Install and run:**
```bash
pip install -r requirements.txt
python src/app.py
```

## Contact

- GitHub: [sanketkarwalink](https://github.com/sanketkarwalink)
- Email: sanketkarwa.inbox@gmail.com