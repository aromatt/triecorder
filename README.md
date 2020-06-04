# triecorder

## Usage

    $ ./triecorder.py -h
    usage: triecorder.py [-h] [-d] [-m MIN_COUNT] [-t FANOUT_THRESHOLD]

    Summarize lines of input.

    optional arguments:
      -h, --help           show this help message and exit
      -d, --debug          Print debug output
      -m MIN_COUNT         Minimum child node count to qualify a node for
                           summarization. Default: 3
      -t FANOUT_THRESHOLD  Minimum fanout at which to summarize. Fanout is defined
                           as immediate_children / total_children. Default: 0.5


## Examples:

```
$ cat data/000.txt
hello
hippo
charles
charmander
charmeleon
charizard

$ cat data/000.txt | ./triecorder.py
char... (5)
hello
hippo
```
