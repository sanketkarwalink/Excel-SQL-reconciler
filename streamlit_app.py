#!/usr/bin/env python3
"""
Entry point for Streamlit Cloud deployment
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main app
try:
    from app import main
    main()
except ImportError:
    # Fallback import
    sys.path.append('src')
    from app import main
    main()
