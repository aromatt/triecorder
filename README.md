# triecorder

## Usage

```
$ ./triecorder.py -h
usage: triecorder.py [-h] [-d] [-m MIN_COUNT] [-t FANOUT_THRESHOLD]
                     [-M MULTIPLIER]

Summarize lines of input.

optional arguments:
  -h, --help           show this help message and exit
  -d, --debug          Print debug output
  -m MIN_COUNT         Minimum total child node count to qualify a node for
                       summarization.
  -t FANOUT_THRESHOLD  Minimum fanout at which to summarize. Fanout is defined
                       as immediate_children / total_children.
  -M MULTIPLIER        Multiplier used to automatically determine
                       summarization parameters. Increase to show more values.
                       Default: 0.33
```

## Examples:

```
# No summarization at all; print raw input (may be out of order)
$ cat data/000.txt | ./triecorder.py -M 1
charles
charmander
charmeleon
charizard
hello
hippo

# Summarize with default automatic tuning
$ cat data/000.txt | ./triecorder.py
h... (2)
char... (5)

# Show more (summarize less)
$ cat data/000.txt | ./triecorder.py -M 0.6
hippo
hello
char... (5)
```
