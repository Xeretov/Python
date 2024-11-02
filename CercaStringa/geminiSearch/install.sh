#!/bin/bash

# Exit on error
set -e

# Check Python3
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install Python 3 and try again."
    exit 1
fi

# Check pip
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Please install pip and try again."
    exit 1
fi

# Create folder
mkdir ./cerca_stringa

# Move to folder
cd  cerca_stringa

# Move files
cp ../cerca.py .
cp ../geminiSearch.py .
cp ../requirements.txt .

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "Installation completed successfully!"
echo "To activate the virtual environment, run: source venv/bin/activate"
