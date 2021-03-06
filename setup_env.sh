#!/usr/bin/env bash

echo "Setting up Environment"

echo "Activating virtual environment"
source venv/bin/activate
echo "virtual environment activated"

echo "Downloading requirements"
pip install -r Flu_Tracker/requirements.txt
echo "Requirements installed"
