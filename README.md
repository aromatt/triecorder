# triecorder

Summarize lines of text.

[![Build Status](https://travis-ci.com/aromatt/triecorder.svg)](https://travis-ci.com/aromatt/triecorder.svg)

## Usage
```
$ ./triecorder.py -h
usage: triecorder.py [-h] [-v] [-m MIN_COUNT] [-t FANOUT_THRESHOLD]
                     [-M MULTIPLIER] [-d DELIMITER]

Summarize lines of input.

optional arguments:
  -h, --help           show this help message and exit
  -v, --verbose        Print trie structure and stats
  -m MIN_COUNT         Minimum total child node count to qualify a node for
                       summarization.
  -t FANOUT_THRESHOLD  Minimum fanout at which to summarize. Fanout is defined
                       as immediate_children / total_children.
  -M MULTIPLIER        Multiplier used to automatically determine
                       summarization parameters. Increase to show more values.
                       Default: 0.33
  -d DELIMITER         Delimiter. Default is None (nodes can split from any
                       letter).
```

## Examples:

```
$ cat data/000.txt
charles
charmander
charmeleon
charizard
hello
hippo

# Summarize with default automatic tuning
$ cat data/000.txt | ./triecorder.py
h ... (2)
char ... (5)

# Show more (summarize less)
$ cat data/000.txt | ./triecorder.py -M 0.5
hippo
hello
char ... (5)
```
