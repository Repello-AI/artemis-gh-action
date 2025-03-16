#!/bin/bash
set -e

# Run the Python script with arguments passed to the Docker container
python /app/main.py "$@"