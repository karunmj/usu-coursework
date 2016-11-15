#!/usr/bin/env python

import sys

countybyparty = {}
countyperc = {}

for line in sys.stdin:
    line = line.strip()
    county, partyid, count = line.split('\t')

    try:
        county = int(county)
    except ValueError:
        continue

    try:
        partyid = int(partyid)
    except ValueError:
        continue

    try:
        count = int(count)
    except ValueError:
        continue            

    try:
        countybyparty[county][partyid] = countybyparty[county][partyid] + count
    except:
        try:
            countybyparty[county][partyid] = count
        except:
            countybyparty[county] = {}        
  
for county in countybyparty:
    #print '%s\t%s' % (county, countybyparty[county])
    a = []
    for party in countybyparty[county]:
        a.append(countybyparty[county][party])
    print '%s\t%s' % (county, float(max(a))/sum(a))        

#for line in sys.stdin:
#    line = line.strip()
#    vote, count = line.split('\t', 1)
#    try:
#        count = int(count)
#    except ValueError:
#        continue
#    try:
#        vote2count[vote] = vote2count[vote]+count
#    except:
#        vote2count[vote] = count

#for vote in vote2count.keys():
#    print '%s\t%s' % (vote, vote2count[vote])

#for county in countyperc.keys():
#    print '%s\t%s' % (county, countyperc[county])
