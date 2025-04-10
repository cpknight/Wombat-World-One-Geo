#!/bin/bash

# Server directory
SERVER_DIR="/home/cpknight/Projects/Wombat-World-One-Geo/server"

# Paper jar file (adjust if version changes later)
PAPER_JAR="$SERVER_DIR/paper-1.21.4-222.jar"

# Check if the server directory exists
if [ ! -d "$SERVER_DIR" ]; then
    echo "Error: Server directory '$SERVER_DIR' not found."
    exit 1
fi

# Check if the Paper jar exists
if [ ! -f "$PAPER_JAR" ]; then
    echo "Error: Paper jar file '$PAPER_JAR' not found."
    exit 1
fi

# Stop any running instance (optional, prevents port conflicts)
echo "Checking for running server instance..."
pkill -f "java.*$PAPER_JAR" 2>/dev/null
sleep 2  # Wait for shutdown

# Change to server directory and launch
cd "$SERVER_DIR" || {
    echo "Error: Could not change to directory '$SERVER_DIR'."
    exit 1
}
echo "Launching Paper server with Geyser from '$PAPER_JAR'..."
java -Xmx2G -Xms1G -jar "$PAPER_JAR" nogui
