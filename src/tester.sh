#!/bin/bash

ITERATIONS=2000
global_count=0
exec_count=0
total_time=0

show_progress() {
    local current=$1
    local total=$2
    local average=$3
    local avg_time=$4
    local width=50
    local percentage=$((current * 100 / total))
    local completed=$((current * width / total))
    local remaining=$((width - completed))
    
    local bar=""
    for ((j=0; j<completed; j++)); do bar+="█"; done
    for ((j=0; j<remaining; j++)); do bar+="░"; done
    
    printf "\r%s -- %3d%% (%d/%d) - Moyenne : %d - Temps : %dms " "$bar" "$percentage" "$current" "$total" "$average" "$avg_time"
}

for ((i=0; i<ITERATIONS; i++)); do
    # Measure execution time
    start_time=$(date +%s%3N)
    
    # Capture both stdout and stderr, check exit status
    if output=$(python src/rubik.py -r 2>>/tmp/error.tmp); then
        end_time=$(date +%s%3N)
        execution_time=$((end_time - start_time))
        
        count=$(echo "$output" | wc -l)
        ((global_count+=count))
        ((total_time+=execution_time))
        ((exec_count++))
    else
        echo "Iteration $((i+1)): Python execution failed with exit code $?" >> error.log
        cat /tmp/error.tmp >> error.log
        echo -e "\nWarning: Error"
        echo "" >> error.log
    fi
    rm /tmp/error.tmp

    if [ $exec_count -gt 0 ]; then
        average=$((global_count / exec_count))
        avg_time=$((total_time / exec_count))
    else
        average=0
        avg_time=0
    fi
    show_progress $((i+1)) $ITERATIONS $average $avg_time

done

if [ $exec_count -gt 0 ]; then
    average=$((global_count / exec_count))
    avg_time=$((total_time / exec_count))
else
    average=0
    avg_time=0
fi
show_progress $ITERATIONS $ITERATIONS $average $avg_time
