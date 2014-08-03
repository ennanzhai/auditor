#!/usr/bin/python

import sys

sourcefile = "tmpHard.xml"
targetfile = "hard.xml"

offending = ["<?", "<!--"]

fin = open(sys.argv[1])
fout = open(sys.argv[2], "w")
for line in fin:
    if True in [item in line for item in offending]:
        continue
    fout.write(line)
fin.close()
fout.close()

