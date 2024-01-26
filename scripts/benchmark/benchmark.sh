#!/bin/bash

# Time on page with 10k lines 
tr -dc "A-Za-z 0-9" < /dev/urandom | fold -w100|head -n 1000000 > scripts/benchmark/sample_project/docs/bigpage.md
size=$(ls -lh scripts/benchmark/sample_project/docs/bigpage.md | awk '{print $5}')


function build_mkdocs {
    local mkdocs_config_file="$1"

    echo "Building: $mkdocs_config_file"
    # Start the timer
    start_time=$(date +%s)
    mkdocs build -q -f "$mkdocs_config_file"
    end_time=$(date +%s)
    elapsed_time=$((end_time - start_time))
    minutes=$((elapsed_time / 60))
    seconds=$((elapsed_time % 60))
    formatted_time="${minutes} mins ${seconds} secs"

    echo "Built $mkdocs_config_file, using a page with size $size. Elapsed time: $formatted_time"
}

mkdocs_config_file="scripts/benchmark/sample_project/mkdocs.yml"
build_mkdocs "$mkdocs_config_file"

mkdocs_config_file="scripts/benchmark/sample_project/mkdocs_no_tablereader.yml"
build_mkdocs "$mkdocs_config_file"

mkdocs_config_file="scripts/benchmark/sample_project/mkdocs_superfences.yml"
build_mkdocs "$mkdocs_config_file"

mkdocs_config_file="scripts/benchmark/sample_project/mkdocs_selected_readers.yml"
build_mkdocs "$mkdocs_config_file"
