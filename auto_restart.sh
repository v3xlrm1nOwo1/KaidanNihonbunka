#!/bin/bash

# Check if a Python script file was provided as an argument
if [ $# -eq 0 ]; then
    echo "Error: No Python script file provided."
    exit 1
fi

# Path to the Python script file provided as an argument
python_script="$1"

# Check if the specified file exists and is a regular file
if [ ! -f "$python_script" ]; then
    echo "Error: File '$python_script' not found or is not a regular file."
    exit 1
fi

# Loop to continuously run the specified Python script
while true; do
    python3 "$python_script"
    echo "Python script stopped. Restarting..."
done
