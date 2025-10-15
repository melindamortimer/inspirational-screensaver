#!/bin/bash
# Helper script to kill hanging screensaver processes

echo "Looking for hanging screensaver processes..."
PIDS=$(ps aux | grep "[p]ython.*main.py" | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "No hanging processes found."
else
    echo "Killing processes: $PIDS"
    kill -9 $PIDS
    echo "Done!"
fi
