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
# Compute the capture frequency matrix for a number of sources 
# Assumption: data sets have unique addresses sorted in string order
# 		(XXX change to numeric sorting?)
#
# $Id: sefasi_capture_data.py 710 2013-11-25 03:55:29Z szander $

import os
import sys 
import getopt
import csv


# index of column with (encrypted) IP
idx = 0
# number of sources
nsources = 0
# output file
ofname = ""
# verbose
verbose = False
# sample rate
srate = 1.0


def keep_going(ends, nsources):
	for i in range(nsources):
		if not ends[i]:
			return(True)
				
	return(False)


def usage():
        print "Usage: " + os.path.basename(sys.argv[0]) + " [-i <index>] -N <sources_cnt> [-o <out_file>] [-r <sample_rate> [-h] [-v] <ip_list1> <ip_list2> [... <ip_listN>]\n" + \
                "\t-i <index> \t\tcolumn index in input files that contains IP addresses\n" + \
                "\t-N <sources_cnt> \tnumber of input files (must be at least 2)\n" + \
                "\t-o <out_file> \t\tif specified the intersect set will be written to file\n" + \
                "\t-r <sample_rate> \t\tsample rate used for sampling the data sources (default: 1.0)\n" + \
                "\t-h \t\t\tshow usage\n" + \
                "\t-v \t\t\tenable verbose mode"


def die(msg, show_usage=False):
        print msg
        if show_usage:
                usage()
        sys.exit(1)

# main

try:
	opts, args = getopt.getopt(sys.argv[1:], "i:N:o:r:hv")
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
	elif o == "-r":
                srate = float(a)
	elif o == "-v":
		verbose = True
	else:
		assert False, "unhandled option " + str(o)

if srate != 1.0 and (srate > 0.5 or srate < 0.0):
        die("Error: sample rate must be 1.0 or between 0.0 and 0.5")

# capture matrix
# first 0...dim columns indicate capture in ith source, last column is frequency
row_dim = pow(2, nsources) - 1
captures = [[0 for col in range(nsources+1)] for row in range(row_dim)]

# fill in combinations
cnt = 1
for i in range(row_dim):
	for j in range(nsources):
		if (cnt & (1 << (nsources - 1 - j))) :
			captures[i][j] = 1 
	cnt += 1

if verbose:
	print("Initial matrix:")
	for row in captures:
		print row

# read all sources 
readers = [None] * nsources
for i in range(nsources):
	readers[i] = csv.reader(open(sys.argv[-1 - i],"rb"), delimiter=' ')

rows = [None] * nsources
totals = [0] * nsources
ends = [False] * nsources
for i in range(nsources):
	rows[i] = readers[i].next()

while (keep_going(ends, nsources)):
	ipv4s = [None] * nsources
	for i in range(nsources):
		ipv4s[i] = rows[i][idx]

	# find smallest IP of source we are not at the end already
	sort_ipv4s = sorted(ipv4s, reverse=False)
	for i in range(nsources):
		end = False
		# check if source ended already 
		for j in range(nsources):
			if cmp(sort_ipv4s[i], ipv4s[j]) == 0:
				end = ends[j]
				break
		if end == False:
			smallest = sort_ipv4s[i]
			break

	curr_entry = 0 
	for i in range(nsources):
		c = cmp(smallest, ipv4s[i])
		if c == 0 and not ends[i] :
			totals[i] += 1
			curr_entry |= (1 << i)

			try:
                        	rows[i] = readers[i].next()
                	except StopIteration:
                        	ends[i] = True
			

	# add one more occurance
	captures[curr_entry - 1][nsources] += 1

# get estimates if sampling was used
if srate < 1.0:
	for row in captures:
		row[nsources] = int(round(float(row[nsources]) / srate, 0))
	
if verbose:
	print("Final matrix:")
for row in captures:
	print ', '.join(map(str,row))

if cmp(ofname, "") != 0:
	writer = csv.writer(open(ofname,"wb"), delimiter=' ')
	for row in captures:
		writer.writerow(row)	

