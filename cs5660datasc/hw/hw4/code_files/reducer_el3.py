#!/usr/bin/env python

import sys

countybyyear2006 = {}
countybyyear2008 = {}
#countyperc = {}

for line in sys.stdin:
    line = line.strip()
    county, partyid2006, partyid2008, count = line.split('\t')

    try:
        county = int(county)
    except ValueError:
        continue

    try:
        partyid2006 = int(partyid2006)
    except ValueError:
        continue

    try:
        partyid2008 = int(partyid2008)
    except ValueError:
        continue            

    try:
        count = int(count)
    except ValueError:
        continue

    try:
        countybyyear2006[county][partyid2006] = countybyyear2006[county][partyid2006] + count
    except:
        try:
            countybyyear2006[county][partyid2006] = count
        except:
            countybyyear2006[county] = {}
    
    try:
        countybyyear2008[county][partyid2008] = countybyyear2008[county][partyid2008] + count
    except:
        try:
            countybyyear2008[county][partyid2008] = count
        except:
            countybyyear2008[county] = {}        
  
for county2006, county2008 in zip(countybyyear2006, countybyyear2008):
    print '%s\t%s\t%s\t%s' % (county2006, countybyyear2006[county2006], county2008, countybyyear2008[county2008])
    #print '%s\t%s' % (county2006, float(countybyyear2008[k])/countybyyear2006 for k in countybyyear2006.viewkeys() & countybyyear2008.viewkeys())
