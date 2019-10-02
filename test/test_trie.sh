#!/bin/bash -e

root=$(cd $(dirname $0)/.. && pwd)

echo
echo '==='
cat $root/data/000.txt | DEBUG=true python3 $root/triecorder.py

echo
echo '==='
cat $root/data/000.txt | MIN_COUNT=3 RATIO=2 python3 $root/triecorder.py
