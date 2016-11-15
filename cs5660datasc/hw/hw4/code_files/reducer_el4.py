#!/usr/bin/env python

import sys

votechange = {}

for line in sys.stdin:
    line = line.strip()
    voterid, party2006, party2008 = line.split('\t')

    try:
        voterid = int(voterid)
    except ValueError:
        continue

    try:
        party2006 = int(party2006)
    except ValueError:
        continue

    try:
        party2008 = int(party2008)
    except ValueError:
        continue            

    try:
        if party2006!=party2008:
            votechange[voterid] = 1
        if part2006==party2008:
            votechange[voterid] = 0
    except:
        pass
               
  
for voter in votechange:
    print '%s\t%s' % (voter, votechange[voter])
