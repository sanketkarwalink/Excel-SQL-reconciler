#!/usr/bin/env python3
"""
Setup configuration for Excel-to-SQL Reconciler

Author: Sanket Karwa
GitHub: https://github.com/sanketkarwa/excel-to-sql-reconciler
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="excel-to-sql-reconciler",
    version="1.0.0",
    author="Sanket Karwa",
    author_email="sanketkarwa.inbox@gmail.com",
    description="AI-powered financial reconciliation tool that reduces month-end GL reconciliation from 6 hours to 30 seconds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sanketkarwa/excel-to-sql-reconciler",
    project_urls={
        "Bug Tracker": "https://github.com/sanketkarwa/excel-to-sql-reconciler/issues",
        "Documentation": "https://github.com/sanketkarwa/excel-to-sql-reconciler#readme",
        "Source Code": "https://github.com/sanketkarwa/excel-to-sql-reconciler",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Accounting",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Framework :: Streamlit",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov>=4.0',
            'flake8>=6.0',
            'black>=23.0',
            'bandit>=1.7',
            'safety>=2.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'excel-sql-reconciler=src.app:main',
        ],
    },
    include_package_data=True,
    package_data={
        'src': ['data/*.csv', 'prompts/*.txt'],
    },
    keywords=[
        'finance', 'accounting', 'reconciliation', 'ai', 'openai', 
        'streamlit', 'data-analysis', 'fintech', 'automation',
        'general-ledger', 'audit', 'excel', 'sql'
    ],
    zip_safe=False,
)
