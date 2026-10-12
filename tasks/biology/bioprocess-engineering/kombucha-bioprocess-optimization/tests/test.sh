#!/usr/bin/env bash
set -e
echo "Running independent verification tests for kombucha pipeline..."
python3 /app/tests/test_verification.py
echo "All verification tests passed successfully!
