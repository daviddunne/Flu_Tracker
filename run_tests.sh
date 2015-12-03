#!/usr/bin/env bash


echo "Starting tests now"
source venv/bin/activate
cd Flu_Tracker

python3 -m discover
