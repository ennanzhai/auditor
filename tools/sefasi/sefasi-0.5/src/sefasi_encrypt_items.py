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
# Encrypt (encrypted) items with commutative RSA 
#
# $Id: sefasi_encrypt_items.py 644 2013-08-15 05:27:44Z szander $

import os
import sys 
import getopt
import csv
import time 
import socket
import struct
import ConfigParser
from Crypto.PublicKey import RSA
from Crypto.PublicKey import pubkey
from Crypto.Util import number

# globals

# column with (encrypted) IP address
idx = 0
# input is ips
input_is_ipv4s = False 
# be verbose
verbose = False
# config file
cfg_fname = ""


# convert decimal dotted quad string to long integer
def dottedQuadToNum(ip):
        return struct.unpack('!L', socket.inet_aton(ip))[0]


def usage():
        print "Usage: " + os.path.basename(sys.argv[0]) + " [-i <index>] [-I] -c <public_config> -p <private_config> [-h] [-v] (-|<item_list>)\n" + \
                "\t-i <index> \t\tcolumn index in input file that contains IP addresses\n" + \
                "\t-I \t\tspecify that the input items are IPv4 addresses\n" + \
                "\t-c <config> \tpublic config file name\n" + \
                "\t-p <private_config> \tprivate config file name\n" + \
                "\t-h \t\t\tshow usage\n" + \
                "\t-v \t\t\tenable verbose mode"


def die(msg, show_usage=False):
        print msg
        if show_usage:
                usage()
        sys.exit(1)

# main

try:
	opts, args = getopt.getopt(sys.argv[1:], "c:i:Ip:hv")
except getopt.GetoptError, err:
	usage()
        die("Error: " + err.msg)

for o, a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-c":
		cfg_fname = a
	elif o == "-i":
		idx = int(a) 
	elif o == "-I":
               	input_is_ipv4s = True 
	elif o == "-p":
		pcfg_fname = a
	elif o == "-v":
		verbose = True
	else:
		assert False, "unhandled option " + str(o)

if cfg_fname == "":
	die("Error: need public config file", True)
if pcfg_fname == "":
	die("Error: need private config file", True)

config = ConfigParser.ConfigParser()
config.readfp(open(cfg_fname))
pconfig = ConfigParser.ConfigParser()
pconfig.readfp(open(pcfg_fname))

if not config.has_option("encryption", "p") or not config.has_option("encryption", "q") :
	die("Error: primes p and q must be defined in public config")

p = long(config.get("encryption", "p"))
q = long(config.get("encryption", "q"))

# get private key
if not pconfig.has_option("encryption", "private_key"):
        die("Error: private key must be defined in private config")

e = long(pconfig.get("encryption", "private_key"))

if p > q:
	(p, q)=(q, p)

phi = (p - 1)*(q - 1)
n = p*q
d=pubkey.inverse(e, phi)

tuple = n, e, d, p, q

if verbose:
	print "p=", p
	print "q=", q
	print "n=", n
	print "e=", e
	print "d=", d

# encrypt without armouring (PKCS)
key = RSA.construct(tuple)
#print(key)

if (cmp(sys.argv[-1], "-") == 0):
        reader = csv.reader(sys.stdin, delimiter=' ')
else:
        reader = csv.reader(open(sys.argv[-1],"rb"), delimiter=' ')

start_time = time.time()
cnt = long(0)
for row in reader:
	ciphertext = ""
	if input_is_ipv4s:
		# encrypt IP
		try:
			#b = number.long_to_bytes(dottedQuadToNum(row[idx]))
                	#(ciphertext,) = key.encrypt(b, 0)
        		(ciphertext,) = key.encrypt(row[idx], 0)
		except IndexError:
                	die("Error: input file has less than index columns")
	else:
		# encrypt encrypted IP
		b = number.long_to_bytes(long(row[0]))
		(ciphertext,) = key.encrypt(b, 0) 

	print(number.bytes_to_long(ciphertext))
	cnt += 1

if verbose:
	print cnt, "addresses"
	print time.time() - start_time, "seconds"

