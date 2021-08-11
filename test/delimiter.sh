#!/bin/bash -e
cat $(dirname $0)/data/001.txt | ./triecorder.py -s -t 0.5 -m 1
echo
cat $(dirname $0)/data/001.txt | ./triecorder.py -s -t 0.5 -m 1 -d'.'
