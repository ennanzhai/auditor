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
# Deterministically sample items 
#
# $Id: sefasi_sample_items.py 644 2013-08-15 05:27:44Z szander $

import os
import sys 
import getopt
import csv
from Crypto.Hash import SHA, MD5 
from Crypto.Util import number
import murmur

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


def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	return type('Enum', (), enums)


def usage():
	print "Usage: " + os.path.basename(sys.argv[0]) + " [-H <hash_function>] [-i <index>] [-r <sample_rate>] [-s <salt>] [-h] [-v] (-|<item_list>)\n" + \
		"\t-H <hash_function> \thash function to be used ('sha1' or 'md5' or 'murmur', default 'murmur')\n" + \
		"\t-i <index> \t\tindex of input file that contains IP addresses\n" + \
		"\t-r <sample_rate> \tsample rate that must be 1.0 or equal smaller 0.5 (default 1.0)\n" + \
		"\t-s <salt> \t\trandom 'salt' that is xored with IP before hashing (default 0)\n" + \
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
	if salt > 0:
		print "Info: using salt value", salt

for row in reader:

	try:
		if not use_salt:
			b = row[idx] 
		else:
			b = row[idx] + str(salt)
	except IndexError:
		die("Error: input file has less than index columns")
	
	if hash_function == Hashes.MURMUR:
	        h = murmur.string_hash(b)

		if int(h) % mod == 0 :
                        print ' '.join(row)
	elif hash_function == Hashes.SHA1:
		h = SHA.new(b)		

		if number.bytes_to_long(h.digest()) % mod == 0 :
                        print ' '.join(row)
	else:
		h = MD5.new(b)

		if number.bytes_to_long(h.digest()) % mod == 0 :
			print ' '.join(row)

