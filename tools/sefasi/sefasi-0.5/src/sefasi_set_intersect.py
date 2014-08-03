#!/usr/bin/python
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
# Get the intersect set of two or more sets of encrypted ip addresses 
# Assumption: both sets have unique addresses sorted in _string order_
#             (XXX change to numeric sorting?) 
#
# $Id: sefasi_set_intersect.py 713 2013-11-25 04:53:59Z szander $

import os
import sys 
import getopt
import csv

# index of column that contains encrypted IPs
idx = 0
# number of input files
nsources = 0
# output the intersect set
ofname = ""
output_intersect = False
# verbose output
verbose = False


def keep_going(ends, nsources):
	for i in range(nsources):
		if not ends[i]:
			return(True)
				
	return(False)


def usage():
        print "Usage: " + os.path.basename(sys.argv[0]) + " [-i <index>] -N <sources_cnt> [-o <out_file>] [-h] [-v] <ip_list1> <ip_list2> [... <ip_listN>]\n" + \
                "\t-i <index> \t\tcolumn index in input files that contains IP addresses\n" + \
                "\t-N <sources_cnt> \tnumber of input files (must be at least 2)\n" + \
                "\t-o <out_file> \t\tif specified the intersect set will be written to file\n" + \
                "\t-h \t\t\tshow usage\n" + \
                "\t-v \t\t\tenable verbose mode"


def die(msg, show_usage=False):
        print msg
        if show_usage:
                usage()
        sys.exit(1)

# main

try:
	opts, args = getopt.getopt(sys.argv[1:], "i:N:o:hv")
except getopt.GetoptError, err:
	usage()
        die("Error: " + err.msg)

for o, a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-i":
		idx = int(a) 
	elif o == "-N":
		nsources = int(a)
	elif o == "-o":
                ofname = a
		output_intersect = True
	elif o == "-v":
		verbose = True
	else:
		assert False, "unhandled option " + str(o)

if idx < 0:
        die("Error: IP column index must be 0 or greater")
if nsources < 2:
        die("Error: Must have at least two input files", True)

# read all sources 
readers = [None] * nsources
for i in range(nsources):
	readers[i] = csv.reader(open(sys.argv[-nsources + i],"rb"), delimiter=' ')

# open output file if we want to store intersect
if output_intersect:
        ofile = open(ofname, "w")

rows = [None] * nsources
totals = [0] * nsources
ends = [False] * nsources
for i in range(nsources):
	rows[i] = readers[i].next()

intersect_cnt = 0
while (keep_going(ends, nsources)):
	ips = [None] * nsources
	for i in range(nsources):
		ips[i] = rows[i][idx]

	# find smallest IP of source we are not at the end already
	sort_ips = sorted(ips, reverse=False)
	for i in range(nsources):
		end = False
		# check if source ended already 
		for j in range(nsources):
			if cmp(sort_ips[i], ips[j]) == 0:
				end = ends[j]
				break
		if end == False:
			smallest = sort_ips[i]
			break
	#print(smallest)

	is_in_intersect = True 
	for i in range(nsources):
		c = cmp(smallest, ips[i])
		if c == 0 and not ends[i] :
			totals[i] += 1

			try:
                        	rows[i] = readers[i].next()
                	except StopIteration:
                        	ends[i] = True
		else:
			is_in_intersect = False
			
	if is_in_intersect:
		intersect_cnt += 1
		if output_intersect:
        		ofile.write(smallest + "\n")

if output_intersect:
        ofile.close()

if verbose:
	for i in range(nsources):
		print "Set", i, ":", totals[i]
print intersect_cnt
