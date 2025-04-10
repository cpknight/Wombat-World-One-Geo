#!/bin/bash

# Server directory and world folder
SERVER_DIR="/home/cpknight/Projects/Wombat-World-One-Geo/server"
WORLD_DIR="$SERVER_DIR/world"

# Backup root directory
BACKUP_ROOT="/home/cpknight/Projects/Wombat-World-One-Geo/world-backups"

# Check if server and world directories exist
if [ ! -d "$SERVER_DIR" ]; then
    echo "Error: Server directory '$SERVER_DIR' not found."
    exit 1
fi
if [ ! -d "$WORLD_DIR" ]; then
    echo "Error: World directory '$WORLD_DIR' not found."
    exit 1
fi

# Check if backup root exists
if [ ! -d "$BACKUP_ROOT" ]; then
    echo "Error: Backup root '$BACKUP_ROOT' not found."
    exit 1
fi

# Find the latest backup (assumes folders like world-backup-YYYYMMDD-HHMMSS)
LATEST_BACKUP=$(ls -d "$BACKUP_ROOT"/world-backup-* 2>/dev/null | sort -r | head -n 1)
if [ -z "$LATEST_BACKUP" ]; then
    echo "Error: No backup folders found in '$BACKUP_ROOT'."
    exit 1
fi

# Stop the server if running
echo "Stopping Paper server if running..."
pkill -f "java.*paper-1.21.4-222.jar" 2>/dev/null
sleep 2  # Give it a moment to shut down

# Copy terrain data from latest backup
echo "Updating terrain from '$LATEST_BACKUP' to '$WORLD_DIR'..."
cp -r "$LATEST_BACKUP/level.dat" "$LATEST_BACKUP/region" "$LATEST_BACKUP/DIM-1" "$LATEST_BACKUP/DIM1" "$WORLD_DIR/"
if [ $? -eq 0 ]; then
    echo "Terrain update completed successfully from '$LATEST_BACKUP'."
else
    echo "Error: Failed to update terrain. Check permissions or disk space."
    exit 1
fi
