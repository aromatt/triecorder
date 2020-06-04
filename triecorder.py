#!/usr/bin/env python3

import sys
import os
import argparse

DEFAULT_FANOUT_THRESHOLD = 0.5
DEFAULT_MIN_COUNT = 3

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

    @property
    def fanout(self):
        return float(max(len(self.children), 1)) / max(self.count, 1)

    def to_str(self, depth=0):
        children_strs = ['  ' * depth + c.to_str(depth + 1)
                         for c in self.children.values()]
        return ("%s (%s, %s, %s)\n" % (self.string, len(self.children),
                                       self.count, round(self.fanout, 3))
                + ''.join(children_strs))

    def summarize(self, fanout_threshold, min_count, prefix=''):
        """Nodes with high fanout are truncated."""
        prefix = prefix + self.string
        if len(self.children) == 0:
            return prefix
        if self.count > min_count and self.string != '' and self.fanout > fanout_threshold:
            return prefix + '... (%s)' % self.count
        return '\n'.join(c.summarize(fanout_threshold, min_count, prefix)
                         for c in self.children.values())

    def __repr__(self):
        return self.to_str()

def main(args):
    parser = argparse.ArgumentParser(description="""Summarize lines of input.""")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                        help='Print debug output')
    debug = os.environ.get('DEBUG', '').lower() == 'true'
    parser.add_argument('-m',
        dest='min_count', type=int,
        default=DEFAULT_MIN_COUNT,
        help='Minimum total child node count to qualify a node for summarization. ' +
             'Default: %s' % DEFAULT_MIN_COUNT)
    parser.add_argument('-t',
        dest='fanout_threshold', type=float,
        default=DEFAULT_FANOUT_THRESHOLD,
        help='Minimum fanout at which to summarize. ' +
             'Fanout is defined as immediate_children / total_children. ' +
             'Default: %s' % DEFAULT_FANOUT_THRESHOLD)
    opts = parser.parse_args(args)

    trie = Trie('')
    for line in sys.stdin.readlines():
        trie.add(line.strip())

    if opts.debug:
        print(trie)

    print(trie.summarize(opts.fanout_threshold, opts.min_count))

if __name__ ==  '__main__':
    main(sys.argv[1:])
