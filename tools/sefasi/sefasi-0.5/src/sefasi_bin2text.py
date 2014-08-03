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
# Convert binary (no row delimiter) to number (stdout)
#
# $Id: sefasi_bin2text.py 644 2013-08-15 05:27:44Z szander $

import os
import sys 
import getopt
from Crypto.Util import number

# globals

# input (binary) file
infile = ""
# size of each fild in bytes
field_size = 4
# be verbose
verbose = False


def usage():
	print "Usage: " + os.path.basename(sys.argv[0]) + " -i <infile> [-f <field_size>] [-h] [-v]\n" + \
		"\t-f <field_size> \t\t\size of each field in binary file in bytes\n" + \
		"\t-i <infile> \t\tbinary input file\n" + \
		"\t-h \t\t\tshow usage\n" + \
		"\t-v \t\t\tenable verbose mode"


def die(msg, show_usage=False):
        print msg
	if show_usage:
        	usage()
        sys.exit(1)

# main

try:
	opts, args = getopt.getopt(sys.argv[1:], "f:i:hv")
except getopt.GetoptError, err:
	usage()
        die("Error: " + err.msg)

for o, a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-i":
		infile = a
	elif o == "-f":
		field_size = int(a)
	elif o == "-v":
		verbose = True
	else:
		assert False, "unhandled option " + str(o)

if cmp(infile, "") == 0:
	die("Error: must specify input file", True)

ifile = open(infile, "rb")

while True:
	b = ifile.read(field_size)
	if b == "":
		break
	t = number.bytes_to_long(b)
	print(t)

ifile.close()
