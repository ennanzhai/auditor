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
# Create two test sets of IPs with defined size and overlap 
# TODO: change from blist to radix tree
#
# $Id: sefasi_test_ipsets.py 644 2013-08-15 05:27:44Z szander $

import os
import sys 
import getopt
import csv
import socket
import struct
import random
from blist import sortedlist

# sample rate
srate = 1
# be verbose
verbose = False
# set sizes
set1_size = 1e6
set2_size = 1e6
# overlap
set_overlap = 1e4
# name prefix for test sets
name_pfx = "testset"
# choose only routed ips
only_routed = False

# sets
set1 = {}
set2 = {}

# subnet lookup structure
starts = sortedlist()
ends = sortedlist()


# implement enum
def enum(*sequential, **named):
        enums = dict(zip(sequential, range(len(sequential))), **named)
        return type('Enum', (), enums)


# convert decimal dotted quad string to long integer
def dottedQuadToNum(ip):
        return struct.unpack('!L', socket.inet_aton(ip))[0]


# convert long int to dotted quad string
def numToDottedQuad(n):
	return socket.inet_ntoa(struct.pack('!L', n))


# insert new subnet
def addSubnet(ip, size):
        if int(size) == 0 or int(size) > 32 :
                return
        start = dottedQuadToNum(ip)
        starts.add(start)
        end = start + pow(2, 32 - int(size)) - 1
        ends.add(end)


# check if subnet already there
def lookupSubnet(ip, convert=True) :
	if convert:
        	ip_num = dottedQuadToNum(ip)
	else:
		ip_num = ip
        idx = starts.bisect_right(ip_num) - 1
        if ((idx < 0) or (idx > len(starts) - 1)):
                return False 
        elif (ip_num <= ends[idx]):
                return True 
        else:
                return False 


# convert set of IP numbers to set of IP strings in dotted notation
def setNumToDottedQuad(ip_num_set):
	tmp = {}
	for k in ip_num_set.iterkeys():
		tmp[numToDottedQuad(k)] = 1

	return tmp


def usage():
	print "Usage: " + os.path.basename(sys.argv[0]) + " -n <set1_size> -N <set2_size> -o <overlap> -p <name_prefix>" + \
		      "-r -h -v [(-|<subnet_list>)]\n" + \
		"\t-n <index> \t\ttarget size of set 1 (default 1e6)\n" + \
		"\t-N <index> \t\ttarget size of set 2 (default 1e6)\n" + \
		"\t-o <index> \t\toverlap of sets (default 1e4)\n" + \
		"\t-p <index> \t\tname prefix (default 'testset)\n" + \
		"\t-r \t\tchoose only routed IPs (if specified a subnet_list must be provided)\n" + \
		"\t-h \t\t\tshow usage\n" + \
		"\t-v \t\t\tenable verbose mode"


def die(msg, show_usage=False):
        print msg
        if show_usage:
                usage()
        sys.exit(1)

# main

Hashes = enum('SHA1', 'MD5', 'MURMUR')

try:
	opts, args = getopt.getopt(sys.argv[1:], "n:N:o:p:r:s:hv")
except getopt.GetoptError, err:
	usage()
        die("Error: " + err.msg)

for o, a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-n":
		set1_size = long(a) 
	elif o == "-N":
                set2_size = long(a)
	elif o == "-o":
                set_overlap = long(a)
	elif o == "-p":
                name_pfx = a
	elif o == "-r":
		only_routed = True
	elif o == "-v":
		verbose = True
	else:
		assert False, "unhandled option " + str(o)

if set_overlap > set1_size:
	die("Error: overlap cannot be larger than size of set 1")
if set_overlap > set2_size:
        die("Error: overlap cannot be larger than size of set 2")

if only_routed :
	if (cmp(sys.argv[-1], "-") == 0):
        	reader = csv.reader(sys.stdin, delimiter=' ')
	else:
        	reader = csv.reader(open(sys.argv[-1],"rb"), delimiter=' ')

	for row in reader:
		if len(row) <= idx:
			die("Error: input file has less than index columns")

		(ip, pfx) = row[idx].split("/", 2)
        	pfx = pfx[0:2] # sometimes no space between subnet and next field!

        	if lookupSubnet(ip) :
        		continue

        	addSubnet(ip, pfx)

		# XXX don't understand this code bit that was in the early version
        	#a = pfx.split(".")
		#pfx = a[0]

min_ip = dottedQuadToNum("0.0.0.0")
max_ip = dottedQuadToNum("255.255.255.255")
if only_routed:
	min_ip = dottedQuadToNum("1.0.0.0")
	max_ip = dottedQuadToNum("223.255.255.255")

while (len(set1) < set1_size):
	rip = random.randint(min_ip, max_ip) 

	if only_routed and not lookupSubnet(rip, False) :
		continue

	if rip not in set1:
		set1[rip] = 1

while (len(set2) < set_overlap):
	#r = random.randint(0, set1_size - 1)
	#rip = set1.keys()[r]

	#if rip not in set2:
        #        set2[rip] = 1

	rip = set1.keys()[len(set2)]
	set2[rip] = 1

while (len(set2) < set2_size):
	rip = random.randint(min_ip, max_ip)

        if only_routed and not lookupSubnet(rip, False) :
                continue

        if rip not in set1 and rip not in set2:
                set2[rip] = 1

# convert to string representation
set1 = setNumToDottedQuad(set1)
set2 = setNumToDottedQuad(set2)

fname = name_pfx + "_1"
set_file = open(fname, "w")
for ip in sorted (set1.iterkeys()):
	set_file.write(ip + "\n")

set_file.close()

fname = name_pfx + "_2"
set_file = open(fname, "w")
for ip in sorted (set2.iterkeys()):
        set_file.write(ip + "\n")

set_file.close()
