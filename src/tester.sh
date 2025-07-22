#!/bin/bash

ITERATIONS=10
global_count=0
exec_count=0

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
done

echo "Moyenne: $(((global_count / exec_count)))"
