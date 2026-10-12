#!/usr/bin/env bash
set -e
echo "Starting kombucha fermentation kinetic and statistical analysis oracle pipeline..."
python3 /app/solution/analyze_fermentation.py
echo "Oracle solution completed successfully. Outputs generated in /app/results/"
