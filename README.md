# triecorder
Summarize lines of input into a concise trie-based view

Example usage:

```
$ cat data/000.txt
hello
hippo
charles
charmander
charmeleon
charizard

$ cat data/000.txt | RATIO=2 MIN_COUNT=3 ./triecorder.py
hello
hippo
char... (5)
```
