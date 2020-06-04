#!/bin/bash -e

root=$(cd $(dirname $0)/.. && pwd)

echo
echo '==='
cat $root/data/000.txt | $root/triecorder.py -d
