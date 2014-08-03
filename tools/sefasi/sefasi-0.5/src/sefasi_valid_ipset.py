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
# Generate sampled valid set of IPs from routing info
# TODO: change from blist to radix tree
#
# $Id: sefasi_valid_ipset.py 644 2013-08-15 05:27:44Z szander $

import os
import sys 
import getopt
import csv
import socket
import struct
import murmur
from blist import sortedlist
from Crypto.Hash import SHA, MD5 
from Crypto.Util import number

# column of input file that has IPs
idx = 0
# sample rate
srate = 1
# random salt value
salt = 0
use_salt = False
# hash function
hash_function_name = "murmur"
hash_function = -1
# be verbose
verbose = False

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
def lookupSubnet(ip) :
        ip_num = dottedQuadToNum(ip)
        idx = starts.bisect_right(ip_num) - 1
        if ((idx < 0) or (idx > len(starts) - 1)):
                return False 
        elif (ip_num <= ends[idx]):
                return True 
        else:
                return False 


def usage():
	print "Usage: " + os.path.basename(sys.argv[0]) + " -H <hash_function> -i <index> -r <sample_rate> -s <salt> -h -v (-|<subnet_list>)\n" + \
		"\t-H <hash_function> \thash function to be used ('sha1' or 'md5' or 'murmur', default 'murmur')\n" + \
		"\t-i <index> \t\tindex of input file that contains IP addresses\n" + \
		"\t-r <sample_rate> \tsample rate, must be equal smaller 0.5 (default 1.0)\n" + \
		"\t-s <salt> \t\trandom 'salt' which is xored with IP before hashing (default 0)\n" + \
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
	opts, args = getopt.getopt(sys.argv[1:], "H:i:r:s:hv")
except getopt.GetoptError, err:
	usage()
        die("Error: " + err.msg)

for o, a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-H":
		hash_function_name = a
	elif o == "-i":
		idx = int(a) 
	elif o == "-r":
                srate = float(a)
	elif o == "-s":
		salt = long(a)
		use_salt = True
	elif o == "-v":
		verbose = True
	else:
		assert False, "unhandled option " + str(o)

if srate != 1.0 and (srate > 0.5 or srate < 0.0):
        die("Error: sample rate must be 1.0 or between 0.0 and 0.5")
if idx < 0:
	die("Error: IP column index must be 0 or greater")

hash_function = Hashes.MURMUR
if cmp(hash_function_name, "sha1") == 0 :
        hash_function = Hashes.SHA1
elif cmp(hash_function_name, "md5") == 0 :
        hash_function = Hashes.MD5
elif cmp(hash_function_name, "murmur") == 0 :
        hash_function = Hashes.MURMUR
else:
        die("Error: hash function must be 'sha1' or 'md5' or 'murmur'")

if (cmp(sys.argv[-1], "-") == 0):
        reader = csv.reader(sys.stdin, delimiter=' ')
else:
        reader = csv.reader(open(sys.argv[-1],"rb"), delimiter=' ')

mod = int(round(1.0 / srate, 0))

if verbose:
	esrate = 1.0 / float(mod)
	print "Info: effective sample rate is", esrate
	if salt>0:
		print "Info: using salt value", salt 


for row in reader:

	try:
		(ip, pfx) = row[idx].split("/", 2)
	except IndexError:
        	die("Error: input file has less than index columns")

        if lookupSubnet(ip) :
        	continue

	pfx = pfx[0:2] # sometimes no space between subnet and next field!
        addSubnet(ip, pfx)

        ipfx = int(pfx)
        if ipfx > 32 :
        	ipfx = 32
	if ipfx == 0:
		continue

	net_start = dottedQuadToNum(ip)
	net_size = pow(2, 32 - ipfx)
	#print net_start, net_size

	for i in range(net_size):
		ip_num = net_start + i	

		if not use_salt:
			b = str(ip_num)
		else:
			b = str(ip_num) + str(salt)

		if hash_function == Hashes.MURMUR:
                	h = murmur.string_hash(b)

                	if long(h) % mod == 0 :
				ip_str = numToDottedQuad(ip_num)
                                print ip_str
        	elif hash_function == Hashes.SHA1:
			h = SHA.new(b)		
	
			if number.bytes_to_long(h.digest()) % mod == 0 :
                                ip_str = numToDottedQuad(ip_num)
                                print ip_str
		else: 
			h = MD5.new(b)

			if number.bytes_to_long(h.digest()) % mod == 0 :
				ip_str = numToDottedQuad(ip_num)
				print ip_str 


