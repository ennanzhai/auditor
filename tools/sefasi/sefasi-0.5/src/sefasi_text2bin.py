#!/usr/local/bin/python
# Copyright (c) 2013 Centre for Advanced Internet Architectures,
# Swinburne University of Technology. 
#
# Author: Sebastian Zander (szander@swin.edu.au)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as 
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# Convert text files with rows to binary (no row delimiter) 
#
# $Id: sefasi_text2bin.py 644 2013-08-15 05:27:44Z szander $

import os
import sys 
import getopt
import csv
from Crypto.Util import number

# output (binary) file
outfile = ""
# be verbose
verbose = False
# size of each element in bytes 
field_size = 4


def usage():
	print "Usage: " + os.path.basename(sys.argv[0]) + " [-f <field_size>] [-h] [-v] -o <outfile> (-|<infile>)\n" + \
		"\t-f <field_size> \t\tsize of each element in  bytes\n" + \
		"\t-o <outfile> \t\tbinary output file\n" + \
		"\t-h \t\t\tshow usage\n" + \
		"\t-v \t\t\tenable verbose mode"


def die(msg, show_usage=False):
        print msg
        if show_usage:
                usage()
        sys.exit(1)

# main

try:
	opts, args = getopt.getopt(sys.argv[1:], "f:o:hv")
except getopt.GetoptError, err:
	usage()
        die("Error: " + err.msg)

for o, a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-f":
                field_size = int(a)
	elif o == "-o":
		outfile = a
	elif o == "-v":
		verbose = True
	else:
		assert False, "unhandled option " + str(o)

if cmp(outfile, "") == 0:
	die("Error: must specify output file", True)

ofile = open(outfile, "wb")

if (cmp(sys.argv[-1], "-") == 0):
        reader = csv.reader(sys.stdin, delimiter=' ')
else:
        reader = csv.reader(open(sys.argv[-1],"rb"), delimiter=' ')

for row in reader:
	# make sure we pad by passing field_size
	b = number.long_to_bytes(row[0], field_size)
	if len(b) > field_size:
		die("Error: input longer than field size")
	ofile.write(b)

ofile.close()
