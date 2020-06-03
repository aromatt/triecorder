#!/bin/bash -e

root=$(cd $(dirname $0)/.. && pwd)

echo
echo '==='
cat $root/data/000.txt | $root/triecorder.py -d

echo
echo '==='
cat $root/data/000.txt | $root/triecorder.py -m 3 -r 2
