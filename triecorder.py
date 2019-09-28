#!/usr/bin/env python3

import fileinput

class Trie:
    def __init__(self, chars):
        self.chars = chars
        self.children = []

    def add_child(self, child):
        assert(isinstance(child, Trie))
        self.children.extend(child)

    def to_str(self):
        return self.

trie = Trie(None)

for line in fileinput.input():
    for c in line.strip():
        print(F"{c}: {ord(c)}")
    print("---"):w

