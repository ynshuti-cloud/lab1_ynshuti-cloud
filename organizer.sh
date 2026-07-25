#!/bin/bash

csv_file="${1:-grades.csv}"    # optional filename arg, defaults to grades.csv
log_file="organizer.log"
csv_header="assignment,group,score,weight"

# Check the CSV exists FIRST, before doing any other work — avoids
# creating the archive dir or computing a timestamp that just gets thrown away
if [ ! -f "$csv_file" ]
then
    echo "Error: $csv_file does not exist."
    exit 1
fi

# Skip archiving if there's no real grade data (empty or header-only)
line_count=$(wc -l < "$csv_file")
if [ "$line_count" -le 1 ]
then
    echo "$csv_file has no grade data to archive. Skipping."
    exit 0
fi

# mkdir -p creates the dir only if missing, and never errors if it already exists
mkdir -p archive

timestamp=$(date +"%Y%m%d-%H%M%S")
new_name="grades_$timestamp.csv"

# Quote variables so filenames with spaces/special characters don't break the command
mv "$csv_file" "archive/$new_name"

# Restore the header row (not just an empty file) so the next batch of
# grades can be added straight away without retyping column names
echo "$csv_header" > "$csv_file"

echo "$timestamp : $csv_file archived as $new_name" >> "$log_file"

# Confirm on screen too — previously the only feedback was the log file
echo "Archived $csv_file as archive/$new_name"
echo "New $csv_file created for the next batch of grades."
