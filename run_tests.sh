#!/usr/bin/env bash


echo "Activating virtual environment"
source venv/bin/activate
echo "virtual environment activated"

echo "Changing directory"
cd Flu_Tracker
echo "Directory changed"

echo "Starting tests now"
python3 -m discover
