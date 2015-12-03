#!/usr/bin/env bash

echo "Activating virtual environment"
source venv/bin/activate
echo "virtual environment activated"

echo "Downloading requirements"
pip install -r requirements.txt
echo "Requirements installed"
