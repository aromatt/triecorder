#!/bin/bash -e
cat $(dirname $0)/data/000.txt | ./triecorder.py -s -v
