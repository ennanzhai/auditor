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
# Generate default sefasi config including public primes p and q
# XXX don't always generate private key?  
#
# $Id: sefasi_getcfg.py 864 2014-05-14 02:30:59Z szander $

import os
import sys 
import getopt
import csv
import math
import random
import ConfigParser
from Crypto.PublicKey import RSA
from Crypto.PublicKey import pubkey
from Crypto.Util import number

# globals

# be verbose
verbose = False

# modulus should be at least 1024bits for security
# key should be at least 256bits for security
keybits = 256
modbits = 256 # modulus bits 
# minimum data set size
min_size = 1000000
# public config
cfg_fname = ""
# config name
name = "example"
# recompute p and q for existing public config
redo_pq = False


def generate_pq(modbits):
	# generate primes p ad q
	# stolen from pycrypt
        p = q = 1L
        while number.size(p*q) < modbits:
                if modbits > 512 :
                        # Note that q might be one bit longer than p if somebody specifies an odd
                        # number of bits for the key. (Why would anyone do that?  You don't get
                        # more security.)
                        p = pubkey.getStrongPrime(modbits>>1, 0, 1e-12, None)
                        q = pubkey.getStrongPrime(modbits - (modbits>>1), 0, 1e-12, None)
                else :
                        p = pubkey.getPrime(modbits>>1, None)
                        q = pubkey.getPrime(modbits - (modbits>>1), None)

	return (p, q)


def usage():
        print "Usage: " + os.path.basename(sys.argv[0]) + " [-c <config>] [-k <keylen>] [-l <min_size>] [-n <name>] [-m <modlen>] [-h] [-v]\n" + \
                "\t-c <config> \t\tpublic config\n" + \
                "\t-k <keylen> \t\tlength of key in bits (default 256)\n" + \
                "\t-l <min_size> \t\tminimum length of dataset in bytes (default 1,000,000)\n" + \
                "\t-n <name> \t\tname of the config\n" + \
                "\t-m <modlen> \t\tlength of modulus in bits (default 256)\n" + \
                "\t-h \t\t\tshow usage\n" + \
                "\t-v \t\t\tenable verbose mode"


def die(msg, show_usage=False):
        print msg
        if show_usage:
                usage()
        sys.exit(1)

# main

try:
	opts, args = getopt.getopt(sys.argv[1:], "c:k:l:m:n:hv")
except getopt.GetoptError, err:
	usage()
        die("Error: " + err.msg)

for o, a in opts:
	if o == "-c":
		cfg_fname = a
	elif o == "-k":
		keybits = long(a)
	elif o == "-l":
                min_size = long(a)
	elif o == "-h":
		usage()
		sys.exit(0)
	elif o == "-n":
		name = a
	elif o == "-m":
		modbits = long(a)
	elif o == "-v":
		verbose = True
	else:
		assert False, "unhandled option " + str(o)

if modbits < 64:
	die("Error: modulus size must be at least 64 bits")
if keybits > modbits:
	die("Error key must not be longer than modulus (field size)")
if cfg_fname != "" and cmp(cfg_fname[len(cfg_fname)-8:len(cfg_fname)], ".pub.cfg"):
	die("Error: public config file name must have extension .pub.cfg");
	

# generate sampling salt
salt = random.getrandbits(64)

# Generate primes p and q
# phi = (n - 1) * (q - 1)

if cfg_fname != "" :
        config = ConfigParser.ConfigParser()
        config.readfp(open(cfg_fname))
	if not config.has_option("encryption", "keylen") or not config.has_option("encryption", "modlen") :
		die("Error: config must have 'keylen' and 'modlen' paramater in section 'encryption'")
	keybits = int(config.get("encryption", "keylen"))
	modbits = int(config.get("encryption", "modlen"))

        if config.has_option("encryption", "p") and config.has_option("encryption", "q") :
        	p = long(config.get("encryption", "p"))
        	q = long(config.get("encryption", "q"))
		# check if compliant 
		bits = math.ceil(math.log(p*q, 2))
		if bits < modbits:
			print "Warning: existing modulus smaller than", modbits, "bits"
			(p, q) = generate_pq(modbits)
			redo_pq = True
	else:
		(p, q) = generate_pq(modbits)
		redo_pq = True
else :
	(p, q) = generate_pq(modbits)


# It's OK for p to be larger than q, but let's be
# kind to the function that will invert it for
# the calculation of u.
if p > q:
        (p, q)=(q, p)

n = p * q
phi = (p - 1)*(q - 1)

# generate encryption key
# we don't generate a decryption key
e = phi
while number.GCD(e, phi) != 1 or e >= n :
	e = number.getRandomNBitInteger(keybits, None) 


stdout = sys.stdout

# Generate public config file
if cfg_fname == "":
	print "Generating public config file"
	fname = name + ".pub.cfg"
	pfname = name + ".priv.cfg"
	sys.stdout = open(fname, 'w')

	print "[sampling]"
	print "sample_rate= 1.0"
	print "salt=", salt
	print ""
	print "[probing]"
	print "probe_detection= no"
	print "valid_sample_rate= 0.05"
	print "valid_generate= no"
	print "min_data_size=", min_size
	print ""
	print "[encryption]"
	print "keylen=", keybits
	print "modlen=", modbits
	print "p=", p
	print "q=", q
elif redo_pq:
	print "Updating p and q in public config"
	pfname = cfg_fname.replace(".pub.cfg", ".priv.cfg")
	reader = csv.reader(open(cfg_fname,"rb"), delimiter='=')
	sys.stdout = open("__tmp.pub.cfg", 'w')
	for row in reader:
		if len(row) < 1:
			print ""
		elif len(row) < 2:
			print row[0]	
		elif row[0] == 'p':
			next
		elif row[0] == 'q':
			next
		else:
			print "=".join(row)
	print "p=", p
	print "q=", q
	os.rename("__tmp.pub.cfg", cfg_fname)
else:
	pfname = cfg_fname.replace(".pub.cfg", ".priv.cfg")

sys.stdout = stdout
print "Generating private config file"

# generate private validset sampling salt
salt = random.getrandbits(64)

# write private config file
sys.stdout = open(pfname, 'w')
print "[probing]"
print "valid_salt=", salt
print "[encryption]"
print "private_key=", e
os.chmod(pfname, 0600)

sys.stdout = stdout
print "Make sure you PROTECT the private config containing the encryption key!"
