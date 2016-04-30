#!/usr/bin/env python

from numpy import rot90, array
import sys

with open(sys.argv[1]) as f:
    line2d = [list(line.rstrip()) for line in f]
    rotated = rot90(array(line2d))
    for row in rotated:
        print ''.join(row)

