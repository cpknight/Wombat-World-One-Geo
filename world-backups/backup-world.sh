#!/bin/bash

# Source world directory (adjust this to your world's path)
WORLD_SRC="/home/cpknight/.minecraft/saves/W0mbit World 1"

# Backup destination (current directory with timestamp)
BACKUP_DIR="$(pwd)/world-backup-$(date +%Y%m%d-%H%M%S)"

# Check if source directory exists
if [ ! -d "$WORLD_SRC" ]; then
    echo "Error: World directory '$WORLD_SRC' not found. Please set the correct path in the script."
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"
if [ $? -ne 0 ]; then
    echo "Error: Could not create backup directory '$BACKUP_DIR'."
    exit 1
fi

# Copy bare essentials
echo "Backing up essentials from '$WORLD_SRC' to '$BACKUP_DIR'..."
cp -r "$WORLD_SRC/level.dat" "$WORLD_SRC/region" "$WORLD_SRC/DIM-1" "$WORLD_SRC/DIM1" "$BACKUP_DIR/"

# Check if copy succeeded
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $BACKUP_DIR"
else
    echo "Error: Backup failed. Check permissions or disk space."
    exit 1
fi
