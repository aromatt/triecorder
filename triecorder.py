#!/usr/bin/env python3

import argparse
import sys

DEFAULT_FANOUT_THRESHOLD = 0.5
DEFAULT_MIN_COUNT = 3
DEFAULT_MULTIPLIER = 0.33

class SuperString:
    def __init__(self, parts=None, delimiter=''):
        self.parts = parts if parts is not None else []
        self.delimiter = delimiter

    def startswith(self, other):
        for i in range(len(other.parts)):
            if self.parts[i] != other.parts[i]:
                return False
        return True

    def __getitem__(self, i):
        if isinstance(i, slice):
            return SuperString(self.parts[i], self.delimiter)
        else:
            return self.parts[i]

    def __hash__(self):
        return hash(tuple(self.parts)) & hash(self.delimiter)

    def __len__(self):
        return len(self.parts)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        return self.parts < other.parts

    @classmethod
    def from_string(cls, string, delimiter):
        return SuperString(string.split(delimiter), delimiter)

    def __repr__(self):
        return self.delimiter.join(self.parts)

class Trie:
    def __init__(self, string=None):
        self.string = string
        self.children = {}
        self.count = 0

    def contains(self, string):
        if self.string is None:
            return False
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

    def _add_child(self, trie):
        self.children[trie.string[0]] = trie
        self.count += 1

    def _split_at(self, i):
        heir = Trie(self.string[i:])
        heir.children = self.children
        heir.count = self.count
        self.children = {}
        self._add_child(heir)
        self.string = self.string[:i]

    def add(self, new_str):
        if self.string is None:
            c = self.string = type(new_str)()
        num_added = 0 # for updating counts
        for i in range(len(new_str)):
            if i == len(self.string):
                rest = new_str[len(self.string):]
                c = self.find_child(rest)
                if c is not None:
                    num_added = c.add(rest)
                    self.count += num_added
                else:
                    self._add_child(Trie(rest))
                    num_added = 1
                break
            if self.string[i] != new_str[i]:
                self._split_at(i)
                self._add_child(Trie(new_str[i:]))
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

    def summarize(self, fanout_threshold, min_count, prefix='', sort=False):
        """Nodes with high fanout are truncated."""
        prefix = prefix + str(self.string)
        if isinstance(self.string, SuperString) and len(self.children) > 0:
            prefix += self.string.delimiter
        if len(self.children) == 0:
            return prefix
        if self.count > min_count and self.string != '' and self.fanout >= fanout_threshold:
            return prefix + ' ... (%s)' % self.count
        child_values = self.children.values()
        if sort:
            child_values = sorted(child_values)
        return '\n'.join(c.summarize(fanout_threshold, min_count, prefix, sort)
                         for c in child_values)

    def __repr__(self):
        return self.to_str()

    def __lt__(self, other):
        return self.string < other.string

def median(items):
    return sorted(items)[int(len(items) / 2)]

def main(args):
    parser = argparse.ArgumentParser(description="""Summarize lines of input.""")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
            help='Print trie structure and stats')
    parser.add_argument('-m', dest='min_count', type=int, default=None,
            help='Minimum total child node count to qualify a node for summarization. ')
    parser.add_argument('-t', '--fanout-threshold', dest='fanout_threshold',
            type=float, default=None,
            help='Minimum fanout at which to summarize. ' +
                 'Fanout is defined as immediate_children / total_children. ')
    parser.add_argument('-M', '--multiplier', dest='multiplier',
            type=float, default=DEFAULT_MULTIPLIER,
            help='Multiplier used to automatically determine summarization parameters. ' +
                 'Increase to show more values. Default: %s' % DEFAULT_MULTIPLIER)
    parser.add_argument('-d', '--delimiter', dest='delimiter', type=str,
            help='Delimiter. Default is None (nodes can split from any letter).')
    parser.add_argument('-s', '--sort', dest='sort', action='store_true',
            help='Sort sibling nodes by their values.')
    opts = parser.parse_args(args)

    trie = Trie()
    for line in sys.stdin.readlines():
        if opts.delimiter:
            string = SuperString.from_string(line.strip(), opts.delimiter)
        else:
            string = line.strip()
        trie.add(string)

    if opts.verbose:
        print(trie)

    if opts.fanout_threshold is None:
        fanouts = [c.fanout for c in trie.children.values() if c.fanout < 1]
        if len(fanouts) > 0:
            opts.fanout_threshold = median(fanouts) * opts.multiplier
        else:
            opts.fanout_threshold = DEFAULT_FANOUT_THRESHOLD

    if opts.min_count is None:
        counts = [c.count for c in trie.children.values()]
        if len(counts) > 0:
            opts.min_count = int(median(counts) * opts.multiplier)
        else:
            opts.min_count = DEFAULT_MIN_COUNT

    print(trie.summarize(opts.fanout_threshold, opts.min_count, sort=opts.sort))

    if opts.verbose:
        print('\n(fanout_threshold: %s, min_count: %s)' %
                (opts.fanout_threshold, opts.min_count))

if __name__ ==  '__main__':
    main(sys.argv[1:])
