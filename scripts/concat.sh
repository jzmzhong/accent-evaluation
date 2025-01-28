#!/bin/bash

# Output file
output="combined.txt"

# Clear the output file if it exists
> "$output"

# Loop through each .txt file in the current directory
for file in *.txt; do
    # Ensure we're processing only files
    if [ -f "$file" ]; then
        # Read the line from the file
        line_content=$(<"$file")
        # Append the prefix and line content to the output file
        echo "$(basename "$file" .txt): $line_content" >> "$output"
    fi
done

