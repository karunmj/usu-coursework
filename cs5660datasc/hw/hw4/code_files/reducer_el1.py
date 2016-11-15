#!/usr/bin/env python

import sys

vote2count = {}

for line in sys.stdin:
    line = line.strip()
    vote, count = line.split('\t', 1)
    try:
        count = int(count)
    except ValueError:
        continue
    try:
        vote2count[vote] = vote2count[vote]+count
    except:
        vote2count[vote] = count

for vote in vote2count.keys():
    print '%s\t%s' % (vote, vote2count[vote])
