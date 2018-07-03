#! /bin/bash

#cd "$1"
for i in {0..397}; do
    #echo "$file"
    python3 run.py csvtest testdb.csv input.h $i actual.txt
    gcc inference_micro_batch.c -o auto.out -lm #m for math
    count=$((`./auto.out`))
    echo $count
    echo $count | cat >> predict.txt
    total_count=$((total_count+count))	
    #if (( $count == 1 )) 
    #then
    #echo $file
    #fi  
done
echo "$total_count"

