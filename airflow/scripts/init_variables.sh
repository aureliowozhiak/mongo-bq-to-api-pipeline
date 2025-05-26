#!/bin/bash

set -e  # Exit on error

echo "Starting Airflow variables initialization..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check required commands
for cmd in airflow; do
    if ! command_exists $cmd; then
        echo "Error: $cmd is required but not installed."
        exit 1
    fi
done

# Function to set Airflow variable with validation and retry
set_airflow_variable() {
    local name=$1
    local value=$2
    local max_attempts=3
    local attempt=1

    echo "Setting $name..."
    while [ $attempt -le $max_attempts ]; do
        if airflow variables set "$name" "$value"; then
            echo "Successfully set $name"
            return 0
        fi
        echo "Attempt $attempt/$max_attempts: Failed to set $name, retrying in 5 seconds..."
        sleep 5
        attempt=$((attempt + 1))
    done

    echo "Error: Failed to set $name after $max_attempts attempts"
    exit 1
}

# Set Airflow variables with validation
echo "Setting Airflow variables..."

# MongoDB variables
set_airflow_variable "MONGO_COLLECTION" "purchases"
set_airflow_variable "MONGO_DB" "ecommerce"

# Data source configuration
set_airflow_variable "DATA_SOURCE" "mongodb"

# Batch processing configuration
set_airflow_variable "BATCH_SIZE" "500"

# API configuration
set_airflow_variable "API_URL" "http://api:8000/api/data"

# Verify variables were set
echo "Verifying variables..."
max_attempts=3
attempt=1
while [ $attempt -le $max_attempts ]; do
    if airflow variables list; then
        break
    fi
    echo "Attempt $attempt/$max_attempts: Failed to list variables, retrying in 5 seconds..."
    sleep 5
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo "Error: Failed to list variables after $max_attempts attempts"
    exit 1
fi

# Test MongoDB connection using Python
echo "Testing MongoDB connection..."
cat > /tmp/test_mongo.py << 'EOF'
from pymongo import MongoClient
import sys

try:
    client = MongoClient('mongodb://root:example@mongodb:27017/')
    # The ismaster command is cheap and does not require auth
    client.admin.command('ismaster')
    print("MongoDB connection successful!")
    sys.exit(0)
except Exception as e:
    print(f"MongoDB connection failed: {str(e)}")
    sys.exit(1)
EOF

max_attempts=3
attempt=1
while [ $attempt -le $max_attempts ]; do
    if python3 /tmp/test_mongo.py; then
        echo "MongoDB connection test successful!"
        break
    fi
    echo "Attempt $attempt/$max_attempts: MongoDB connection test failed, retrying in 5 seconds..."
    sleep 5
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo "Error: MongoDB connection test failed after $max_attempts attempts"
    exit 1
fi

echo "Airflow variables initialized successfully!" 