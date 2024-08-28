#!/bin/sh

for i in *.jpg; do
    echo "Processing $i"
    python ./convert.py $i sq-$i
done
