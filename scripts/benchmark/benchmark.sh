#!/bin/bash

# Time on page with 10k lines 
tr -dc "A-Za-z 0-9" < /dev/urandom | fold -w100|head -n 100000 > scripts/benchmark/sample_project/docs/bigpage.md

echo "running mkdocs build.."
# Start the timer
start_time=$(date +%s)

# Time this command
mkdocs build -f scripts/benchmark/sample_project/mkdocs.yml

# Calculate the elapsed time
end_time=$(date +%s)
elapsed_time=$((end_time - start_time))

# Calculate minutes and seconds
minutes=$((elapsed_time / 60))
seconds=$((elapsed_time % 60))

# Format the time as X mins Y secs
formatted_time="${minutes} mins ${seconds} secs"

# Write the formatted time to a text file
# echo "Elapsed Time: $formatted_time" > scripts/time_report.txt


size=$(ls -lh scripts/benchmark/sample_project/docs/bigpage.md | awk '{print $5}')

echo "Mkdocs build completed, using a page with size $size. Elapsed time: $formatted_time"
