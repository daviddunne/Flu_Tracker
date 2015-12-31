#!/usr/bin/env bash

echo "Changing directory to project root"
cd Flu_Tracker
echo "Directory changed"


echo "Starting tests now"
python3 -m discover
