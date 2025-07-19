#!/bin/bash

ITERATIONS=100
global_count=0
exec_count=0

for ((i=0; i<ITERATIONS; i++)); do
    ((exec_count++))
    count=$(python src/rubik.py -r | wc -l)
    ((global_count+=count))
done

echo $(echo "scale=2; $global_count / $exec_count" | bc)