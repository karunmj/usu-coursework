#!/usr/bin/env python

import sys

for record in sys.stdin:
    record = record.strip()
    print '%s\t%s\t%s\t%s' % (record.split('\t')[1], record.split('\t')[2], record.split('\t')[5], "1")
