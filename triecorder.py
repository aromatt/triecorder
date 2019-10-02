#!/usr/bin/env python3

import fileinput
import sys
import os

DEFAULT_RATIO = 1000
DEFAULT_MIN_COUNT = 15

class Trie:
    def __init__(self, string):
        self.string = string
        self.children = {}
        self.count = 0

    def contains(self, string):
        if self.string == string:
            return True
        if self.string.startswith(string):
            return True
        if string.startswith(self.string):
            rest = string[len(self.string):]
            c = self.find_child(rest)
            if c is None:
                return False
            return c.contains(rest)
        return False

    def find_child(self, string):
        return self.children.get(string[0])

    def add_child(self, trie):
        self.children[trie.string[0]] = trie
        self.count += 1

    def split_at(self, i):
        heir = Trie(self.string[i:])
        heir.children = self.children
        heir.count = self.count
        self.children = {}
        self.add_child(heir)
        self.string = self.string[:i]

    def add(self, new_str):
        assert(isinstance(new_str, str))
        num_added = 0
        for i in range(len(new_str)):
            if i == len(self.string):
                rest = new_str[len(self.string):]
                c = self.find_child(rest)
                if c is not None:
                    num_added = c.add(rest)
                    self.count += num_added
                else:
                    self.add_child(Trie(rest))
                    num_added = 1
                break
            if self.string[i] != new_str[i]:
                self.split_at(i)
                self.add_child(Trie(new_str[i:]))
                num_added = 2
                break
        return num_added

    def to_str(self, depth=0):
        children_strs = ['  ' * depth + c.to_str(depth + 1)
                         for c in self.children.values()]
        return F"{self.string} ({self.count}, {len(self.children)})\n" + ''.join(children_strs)

    # Nodes with high fan-out, i.e. a low count/children ratio, are truncated.
    def summarize(self, prefix='', ratio=DEFAULT_RATIO, min_count=DEFAULT_MIN_COUNT):
        prefix = prefix + self.string
        if len(self.children) == 0:
            return prefix
        if self.count > min_count \
                and self.string != '' \
                and float(max(self.count, 1)) / max(len(self.children), 1) < ratio:
            return prefix + F'... ({self.count})'
        return '\n'.join(c.summarize(prefix, ratio=ratio, min_count=min_count)
                         for c in self.children.values())

    def __repr__(self):
        return self.to_str()

def test_trie():
    trie = Trie('')
    trie.add('hi')
    trie.add('hip')
    trie.add('help')
    trie.add('hole')
    trie.add('hop')
    trie.add('charlie')
    trie.add('charmander')
    trie.add('charmeleon')
    print(trie)

def main():
    debug = os.environ.get('DEBUG', '').lower() == 'true'
    ratio = int(os.environ.get('RATIO', DEFAULT_RATIO))
    min_count = int(os.environ.get('MIN_COUNT', DEFAULT_MIN_COUNT))

    trie = Trie('')
    for line in fileinput.input():
        trie.add(line.strip())

    if debug:
        print(trie)

    print(trie.summarize(ratio=ratio, min_count=min_count))

if __name__ ==  '__main__':
    main()
