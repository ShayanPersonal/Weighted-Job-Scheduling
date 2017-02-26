#!/usr/bin/env python3
import sys

fn = open(sys.argv[1], "w")
for i in range(50000):
    fn.write("%d %d %d\n" % (i, i+1, i+2))