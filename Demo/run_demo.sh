#!/bin/bash
# Run script for TribalLink Demo
# Team TechTribe – Pemiya Rishikesh Institute of Technology

# Optional: activate virtual environment if exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Starting TribalLink Flask server..."
python3 app.py
