#!/bin/bash -e

root=$(cd $(dirname $0)/.. && pwd)

echo
echo '==='
cat $root/test/data/000.txt | $root/triecorder.py -v

echo
echo '==='
cat $root/test/data/001.txt | $root/triecorder.py -t 0.5 -m 1

echo
echo '==='
cat $root/test/data/001.txt | $root/triecorder.py -t 0.5 -m 1 -d'.'
