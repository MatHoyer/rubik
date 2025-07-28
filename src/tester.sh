#!/bin/bash

ITERATIONS=100
global_count=0
exec_count=0

show_progress() {
    local current=$1
    local total=$2
    local average=$3
    local width=50
    local percentage=$((current * 100 / total))
    local completed=$((current * width / total))
    local remaining=$((width - completed))
    
    local bar=""
    for ((j=0; j<completed; j++)); do bar+="█"; done
    for ((j=0; j<remaining; j++)); do bar+="░"; done
    
    printf "\r[%s] %3d%% (%d/%d) - Moyenne : %d " "$bar" "$percentage" "$current" "$total" "$average"
}

for ((i=0; i<ITERATIONS; i++)); do
    # Capture both stdout and stderr, check exit status
    if output=$(python src/rubik.py -r 2>>/tmp/error.tmp); then
        count=$(echo "$output" | wc -l)
        ((global_count+=count))
        ((exec_count++))
    else
        echo "Iteration $((i+1)): Python execution failed with exit code $?" >> error.log
        cat /tmp/error.tmp >> error.log
        rm /tmp/error.tmp
        echo "" >> error.log
    fi

    if [ $exec_count -gt 0 ]; then
        average=$((global_count / exec_count))
    else
        average=0
    fi
    show_progress $((i+1)) $ITERATIONS $average

done

if [ $exec_count -gt 0 ]; then
    average=$((global_count / exec_count))
else
    average=0
fi
show_progress $ITERATIONS $ITERATIONS $average
