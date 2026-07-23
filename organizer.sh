#!/bin/bash

# organizer.sh - Archives grades.csv with a timestamp, resets it to a
# fresh empty file, and logs the action to organizer.log.

SOURCE_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# Edge case: source file missing
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' not found. Nothing to archive."
    exit 1
fi

# Check if archive directory exists; create it if not
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
fi

# Generate a timestamp string
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# Build the new archived filename
ARCHIVED_NAME="grades_$TIMESTAMP.csv"

# Move the original file into the archive directory with its new name
mv "$SOURCE_FILE" "$ARCHIVE_DIR/$ARCHIVED_NAME"

# Create a new, empty grades.csv so the workspace is ready for next batch
touch "$SOURCE_FILE"

# Log the archiving details, appending to organizer.log
echo "[$TIMESTAMP] Original: $SOURCE_FILE | Archived as: $ARCHIVE_DIR/$ARCHIVED_NAME" >> "$LOG_FILE"

echo "Archived '$SOURCE_FILE' as '$ARCHIVE_DIR/$ARCHIVED_NAME'."
echo "A fresh, empty '$SOURCE_FILE' has been created."
