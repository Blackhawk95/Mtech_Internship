#! /bin/bash

#cd "$1"
for file in $1/*; do
    #echo "$file"
    python3 run.py $2 "$file" input.h
    gcc inference_micro_batch.c -o auto.out -lm #m for math
    count=$((`./auto.out`))
    total_count=$((total_count+count))	
    #if (( $count == 1 )) 
    #then
    echo $file
    #fi  
done
echo "$total_count"

