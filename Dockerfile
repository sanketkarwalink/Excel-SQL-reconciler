# Excel-to-SQL Reconciler Docker Image
# Author: Sanket Karwa
# GitHub: https://github.com/sanketkarwa/excel-to-sql-reconciler

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY .streamlit/ ./.streamlit/
COPY generate_data.py .
COPY run_app.sh .

# Make scripts executable
RUN chmod +x run_app.sh

# Generate sample data
RUN python generate_data.py

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Expose port
EXPOSE 8501

# Set metadata labels
LABEL maintainer="Sanket Karwa <sanketkarwa.inbox@gmail.com>"
LABEL version="1.0.0"
LABEL description="AI-powered Excel-to-SQL reconciliation tool"
LABEL repository="https://github.com/sanketkarwa/excel-to-sql-reconciler"

# Start the application
CMD ["python", "-m", "streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
