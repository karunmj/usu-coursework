#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    for word in line.lower().split():
        if str(word) == str(word)[::-1]:
            print '%s\t%s' % (word, "1")
