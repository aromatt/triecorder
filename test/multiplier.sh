#!/bin/bash -e
cat $(dirname $0)/data/000.txt | ./triecorder.py -s -M 1
echo
cat $(dirname $0)/data/000.txt | ./triecorder.py -s -M 0.5
echo
cat $(dirname $0)/data/000.txt | ./triecorder.py -s -M 0
