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
# Main script for secure fast set intersection 
#
# $Id: sefasi_main.py 721 2014-01-06 07:34:27Z szander $

import os
import sys 
import getopt
import csv
import math
import subprocess
import ConfigParser
import StringIO
from Crypto.Util import number

# globals

# be verbose
verbose = False
# public config
cfg_fname = ""
# private config
pcfg_fname = ""
# action we want to do
action = ""
# config name
cfg_name = "example"
# intersect how many data sets
intersect_cnt = 2
# options passed to tools
tool_options = ""
# use fast C implementations
fast = False


# get our own path
def get_path():
	# get our location 
	return os.path.dirname(os.path.realpath(sys.argv[0]))


# check if program exists
def prog_exists(program):
	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

	fpath, fname = os.path.split(program)
	#print fpath, fname
	if fpath:
		if is_exe(program):
			return True 
	else:
		exe_file = os.path.join(get_path(), program)
                if is_exe(exe_file):
                        return True
		for path in os.environ["PATH"].split(os.pathsep):
			path = path.strip('"')
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return True

	return False


# count total number of data items in file (assuming one item per line)
def total_cnt(fname):
	path = get_path()
	cmd = ["wc", "-l", fname]
	res = ""
	subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        while True:
                out = subproc.stdout.read()
                if not out:
                        break
                if out != "":
                        res += out
	a = res.strip().split(' ')

        return long(a[0]) 


# count total number of _unique_ data items in file (assuming one item per line)
def total_unique_cnt(fname):
	path = get_path()
	cmd = "cat " + fname  + " | LC_ALL=C sort -u | wc -l"
	res = ""
	subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	while True:
		out = subproc.stdout.read()
		if not out:
			break
                if out != "":
                        res += out

	a = res.strip().split(' ')

	return long(a[0])


# get total count from file fname (first line)
def get_total_cnt(fname):
	cnt = 0
	fname = fname.replace(".encperm","") # take the basename
	with open(fname + ".size", 'r') as f:
		cnt = long(f.readline())
	return cnt


# sample file fname (use murmur hash)
def sample(fname, srate, salt, options=""):
	path = get_path()
	out_fname = fname + ".sample"
	if options == "":
		if not fast:
			cmd = [path + "/sefasi_sample_items.py", "-H", "murmur", "-r", str(srate), "-s", str(salt), fname]	
		else:
			cmd = [path + "/sefasi_sample_items", "-H", "murmur", "-r", str(srate), "-s", str(salt), fname]	
	else:
		if not fast:
        		cmd = [path + "/sefasi_sample_items.py", options, "-H", "murmur", "-r", str(srate), "-s", str(salt), fname]
		else:
        		cmd = [path + "/sefasi_sample_items", tool_options, "-H", "murmur", "-r", str(srate), "-s", str(salt), fname]
	if verbose:
		print(cmd)
        with open(out_fname, 'w') as outfile:
        	subprocess.call(cmd, stdout=outfile)
	return out_fname


# get valid sample (use murmur hash)
def valid_sample(fname, srate, salt, options=""):
	path = get_path()
        out_fname = fname + ".sample"
	if options == "":
		cmd = [path + "/sefasi_valid_ipset.py", "-H", "murmur", "-r", str(srate), "-s", str(salt), fname]
	else:
        	cmd = [path + "/sefasi_valid_ipset.py", options, "-H", "murmur", "-r", str(srate), "-s", str(salt), fname]
	if verbose:
        	print(cmd)
        with open(out_fname, 'w') as outfile:
                subprocess.call(cmd, stdout=outfile)
        return out_fname


# encrypt and permute IP list
def encrypt_and_permute(fname, cfg_fname, pcfg_fname, options=""):
	path = get_path()
	out_fname = fname + ".enc"
	if options == "":
		if not fast:
			cmd = [path + "/sefasi_encrypt_items.py", "-c", cfg_fname, "-p", pcfg_fname, fname]
		else:
			cmd = [path + "/sefasi_encrypt_items", "-c", cfg_fname, "-p", pcfg_fname, fname]
	else:
		if not fast:
        		cmd = [path + "/sefasi_encrypt_items.py", options, "-c", cfg_fname, "-p", pcfg_fname, fname]
		else:
        		cmd = [path + "/sefasi_encrypt_items", options, "-c", cfg_fname, "-p", pcfg_fname, fname]
	if verbose:
		print(cmd)
        with open(out_fname, 'w') as outfile:
        	subprocess.call(cmd, stdout=outfile)
        fname = out_fname 
        out_fname = fname + "perm"
	# the -u for sort enforces sets, i.e. unique elements to prevent multiple elements attack/leakage
        cmd = "cat " + fname + " | LC_ALL=C sort -u > " + out_fname
        os.system(cmd)
	os.remove(fname) # remove the encrypted but not permuted file

       	return out_fname 


# intersect multi-encrypted files in array fnames
def intersect(fnames):
	path = get_path()
	sizes = [0] * len(fnames)
	if not fast:
		cmd = [path + "/sefasi_set_intersect.py", "-N", str(len(fnames)),"-v"] + fnames 
	else:
		cmd = [path + "/sefasi_set_intersect", "-N", str(len(fnames)),"-v"] + fnames
	if verbose:
		print(cmd)
	res = ""
	#subproc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	while True:
		out = subproc.stdout.read()
		if not out:
        		break
		if out != "":
			res += out
	# res contains one line per data set containing the (sampled) sizes
	# plus the last line contains the intersection size
	buf = StringIO.StringIO(res)
	for i in range(len(fnames)):
		line = buf.readline()
		a = line.split(':')
		sizes[i] = long(a[1])	
	int_size = long(buf.readline())

	return (int_size, sizes)


# compute z-value based on 1-alpha
def z_value(oma, twosided=True):
	if oma == 0.95:
		if twosided:
               		z = 1.96
		else:
			z = 1.6449
        elif oma == 0.99:
		if twosided:
                	z = 2.5758
		else:
			z = 2.3263
        elif oma == 0.999:
		if twosided:
                	z = 3.2905
		else:
			z = 3.0902
	elif oma == 0.9999:
		if twosided:
			z = 3.8906
		else:
			z = 3.719
	else:
		z = 1.96 

	return z

# Binomial std error, mean and CI

def binom_std_err(n, p):
	return math.sqrt(n * p * (1 - p))


def binom_mean(n, p):
	return (n * p)


def binom_cint(n, p, one_minus_alpha, twosided=True):
	z = z_value(one_minus_alpha, twosided) 
        m = binom_mean(n, p)
        se = binom_std_err(n, p)
        return (round(m - z * se, 0), round(m + z * se, 0))


def usage():
        print "Usage: " + os.path.basename(sys.argv[0]) + " -a <action> -c <public_config> -p <priv_config> [-n <cfg_name>] " + \
		      "[-N <intersect_cnt>] [-o <tool_options>] [-hfv] <file1> <file2> ...\n" + \
                "\t-a <action> \t\tactions: config, init_enc, valid_enc, valid_check, data_enc, intersect\n" + \
		"\t-c <public_config> \tname of public configuration file\n" + \
		"\t-f \t\t\tuse fast C implementations for sampling, encryption and intersection\n" + \
		"\t-p <private_config> \tname of private configuration file\n" + \
		"\t-n <cfg_name> \tname of config to generate (only used for 'config' action)\n" + \
		"\t-N <intersect_cnt> \tnumber of data sets to intersect (only used for 'intersect' action)\n" + \
		"\t-o <tool_options> \toptions passed to the tool used for the action (e.g sefasi_encrypt_items.py)\n" + \
                "\t-h \t\t\tshow usage\n" + \
                "\t-v \t\t\tenable verbose mode\n" + \
		"\n" + \
		"\tFiles that need to be provided depend on action:\n" + \
		"\tinit_enc: [valid_set] <data_set>\n" + \
		"\tvalid_enc: <valid_set>\n" + \
		"\tvalid_check: <valid_set1> <valid_set2>\n" + \
		"\tdata_enc: [valid_set] <data_set>\n" + \
		"\tintersect: <data_set1> <data_set2> ... <data_setN>"


def die(msg, show_usage=False):
        print msg
        if show_usage:
                usage()
        sys.exit(1)

# main

# check for all tool dependencies
tools = ['wc', 'sort', 'sefasi_sample_items.py', 'sefasi_encrypt_items.py', 'sefasi_valid_ipset.py', 'sefasi_set_intersect.py', 'sefasi_getcfg.py']

for tool in tools:
	if not prog_exists(tool):
		die("Error: need tool " + tool) 

try:
	opts, args = getopt.getopt(sys.argv[1:], "a:c:n:N:p:o:hfv")
except getopt.GetoptError, err:
	usage()
        die("Error: " + err.msg)

for o, a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-c":
		cfg_fname = a
	elif o == "-f":
		fast = True
	elif o == "-p":
		pcfg_fname = a
	elif o == "-a":
		action = a 
	elif o == "-n":
		cfg_name = a
	elif o == "-N":
		intersect_cnt = int(a)
	elif o == "-o":
		# currently this option is not used
                tool_options = a
	elif o == "-v":
		verbose = True
	else:
		assert False, "unhandled option " + str(o)

if fast:
	fast_tools = ['sefasi_sample_items', 'sefasi_encrypt_items', 'sefasi_set_intersect']

	for tool in fast_tools:
        	if not prog_exists(tool):
                	die("Error: need tool " + tool)

if action == "":
	die("Error: need action", True)

if cmp(action, "config") != 0 and cfg_fname == "":
	die("Error: need config for all actions except 'config' action")

if (cmp(action, "init_enc") == 0 or cmp(action, "valid_enc") == 0 or cmp(action, "data_enc") == 0) and pcfg_fname == "":
	die("Error: need private config for encryption")

if cmp(action, "config") != 0:
	config = ConfigParser.ConfigParser()
	try:
		config.readfp(open(cfg_fname))
	except IOError:
		die("Error: can't access public config file '" + cfg_fname + "'")
if cmp(action, "init_enc") == 0:
        pconfig = ConfigParser.ConfigParser()
	try:
        	pconfig.readfp(open(pcfg_fname))
	except IOError:
		die("Error: can't access private config file '" + pcfg_fname + "'")

if cmp(action, "config") == 0:
	# create config files
	path = get_path()
	if cfg_fname != "":
		cmd = [path + "/sefasi_getcfg.py", "-c", cfg_fname, "-n", cfg_name]
	else:
		cmd = [path + "/sefasi_getcfg.py", "-n", cfg_name]
	if verbose:
		print(cmd)
	subprocess.call(cmd)

elif cmp(action, "init_enc") == 0:
	# sampling and encryption of IPs in the clear
	# also if we use valid sets, sampling and encryption of valid set
	probing_detect = False
	valid_srate = 1.0
	valid_fname = ""
	# data file
	fname = sys.argv[-1]
	data_srate = 1.0
	salt = 0
	valid_generate = False 
	min_size = 1e6

	if config.has_option("probing", "probe_detection") :
		if cmp(config.get("probing", "probe_detection"), "yes") == 0:
			probing_detect = True
			if config.has_option("probing", "valid_sample_rate"):
				valid_srate = float(config.get("probing", "valid_sample_rate"))			
				if abs((1.0 / valid_srate) - int(1.0 / valid_srate)) > 0.01 :
					sug_rate = 1.0 / math.ceil(1.0 / valid_srate)
                        		die("Error: valid set sample rate inverse must be an integer" + \
						", e.g use valid_srate= " + str(sug_rate))
				if pconfig.has_option("probing", "valid_salt"):
                                	valid_salt = long(pconfig.get("probing", "valid_salt"))
				else:
					die("Error: valid set salt must be defined in private config")
			if config.has_option("probing", "valid_generate"):
                                if cmp(config.get("probing", "valid_generate"), "yes") == 0:
					valid_generate = True
			valid_fname = sys.argv[-2]
	if config.has_option("sampling", "sample_rate"):
		data_srate = float(config.get("sampling", "sample_rate"))
		if abs((1.0 / data_srate) - int(1.0 / data_srate)) > 0.01 :
			sug_rate = 1.0 / math.ceil(1.0 / valid_srate)
			die("Error: data set sample rate inverse must be an integer" + \
				", e.g. use srate= " + str(sug_rate))
		if config.has_option("sampling", "salt"):
			salt = long(config.get("sampling", "salt"))

	# I'm not sure if we need the following check, but a higher valid sample rate does not make sense
	if probing_detect:
		if valid_srate > data_srate:
			die("Error: valid set sample rate should be smaller than data set sample rate")

	if config.has_option("probing", "min_data_size") :
                min_size = long(config.get("probing", "min_data_size"))

	# check if proper set (and not multiset)

	# check size
	print("Counting number of IPs")
	cnt = total_cnt(fname)
	if cnt < min_size:
		die("Data set is too small (less than " + str(min_size) + " entries) -> ABORT")

	unique_cnt = total_unique_cnt(fname)
	if unique_cnt < cnt:
		die("Data is not a proper set, there are " + str(cnt) + " items, but only " + str(unique_cnt) + \
			" unique items -> ABORT")

	with open(fname + ".size", 'w') as f:
                f.write(str(cnt))

	# generate sampled valid set
	if probing_detect:
		if valid_generate:
			print("Generating (sampled) valid set, this may take a while...")
			valid_fname = valid_sample(valid_fname, valid_srate, valid_salt)
		else:
			print("Using existing valid set " + valid_fname)
			if valid_srate != 1.0:
				print("Sampling existing valid set " + valid_fname)
				valid_fname = sample(valid_fname, valid_srate, valid_salt)

	if data_srate != 1.0:
		print("Sampling data set")
		fname = sample(fname, data_srate, salt)

	if probing_detect:
		print("Encrypting and permuting valid set")
		valid_fname = encrypt_and_permute(valid_fname, cfg_fname, pcfg_fname, "-I")

	print("Encrypting and permuting data set")
	fname = encrypt_and_permute(fname, cfg_fname, pcfg_fname, "-I")

	# remove .sample from file name so we get same name regardless of sampled or not
	if data_srate != 1.0:
		nfname = fname.replace(".sample", "")
		os.rename(fname, nfname)
		fname = nfname

	if valid_srate != 1.0:
                nfname = valid_fname.replace(".sample", "")
                os.rename(valid_fname, nfname)
                valid_fname = nfname

	print("Initial encrypting and permuting done")
	if probing_detect:
		print "Send " + valid_fname + " to the other party"
	else:
		print "Send " + fname + " to the other party"

elif cmp(action, "valid_enc") == 0:
	# valid set encryption
	valid_fname = sys.argv[-1]

	print("Encrypting and permuting valid set")
	valid_fname = encrypt_and_permute(valid_fname, cfg_fname, pcfg_fname)
	print "Return " + valid_fname + " to the other party"

elif cmp(action, "data_enc") == 0:
	# IP data encryption
        fname = sys.argv[-1]
	min_size = 1e6

	# first we do a size check

	if config.has_option("probing", "min_data_size") :
		min_size = long(config.get("probing", "min_data_size"))

	# get the actual count, don't trust the .size file
	cnt = total_cnt(fname)

	# with sampling we need to check is size looks ok statistically
	if config.has_option("sampling", "sample_rate"):
                data_srate = float(config.get("sampling", "sample_rate"))
	if data_srate < 1.0:
                alpha=0.001
                cint = binom_cint(cnt / data_srate, data_srate, 1-alpha, False)
		est_cnt = long(round(cint[0] / data_srate))
		print "Size of unsampled data set >= " + str(est_cnt) + " (" + str(1-alpha) + " CI)"
	else:
		est_cnt = cnt
		
	if est_cnt < min_size:
		die("Data set is too small (less than " + str(min_size) + " entries) -> ABORT")

	unique_cnt = total_unique_cnt(fname)
	if unique_cnt < cnt:
		print "Warning: some duplicate encrypted elements will be removed"

	print("Encrypting and permuting data set")
        fname = encrypt_and_permute(fname, cfg_fname, pcfg_fname)
	if config.has_option("probing", "probe_detection") and \
           cmp(config.get("probing", "probe_detection"), "yes") == 0:
		valid_srate = 1.0
		data_srate = 1.0
		if config.has_option("probing", "valid_sample_rate"):
                	valid_srate = float(config.get("probing", "valid_sample_rate"))
		if config.has_option("sampling", "sample_rate"):
                        data_srate = float(config.get("sampling", "sample_rate"))
		valid_fname = sys.argv[-2]

		print("Check for probing attack")
		(isec_size, sizes) = intersect([valid_fname, fname])
		#print isec_size, sizes

		if valid_srate==1.0:
			if isec_size==sizes[1]:
				print "Dataset of other party is valid"
				print "Return " + fname + " to the other party"
			else:
				die("Possible probing attack -> ABORT")
		else:
			# compute lower bound of confidence interval
			alpha=0.001
			valid_est = long(isec_size/valid_srate)
			valid_est_serr = long(round(binom_std_err(sizes[1], valid_srate) / valid_srate))
			cint = binom_cint(sizes[1], valid_srate, 1-alpha, False)

			if isec_size > cint[0]:
				print "Dataset of other party is valid (estimated valid items " + str(valid_est) + \
					"+-" + str(valid_est_serr) + ", with " + str(1-alpha) + " CI should be >= " + str(long(cint[0]/valid_srate)) + ")"
				print "Return " + fname + " to the other party"
                        else:
                                die("Possible probing attack (estimated valid items " + str(valid_est) + "+-" + str(valid_est_serr) + \
					", with " + str(1-alpha) + " CI should be >= " + str(long(cint[0]/valid_srate)) + ") -> ABORT")
	else:
        	print "Return " + fname + " to the other party"

elif cmp(action, "valid_check") == 0:
	# check if the valid sets for consistency (overlap) 
	# first one should be local data set
	# assume we do a pairwise check
	valid_name1 = sys.argv[-2]
	valid_name2 = sys.argv[-1]

	print("Checking valid sets for consistency")
	(isec_size, sizes) = intersect([valid_name1, valid_name2])
	if isec_size == sizes[0]:	
		print "Valid sets overlap 100%"
	else:
		overp = float(isec_size) / float(sizes[0]) * 100
		die("Valid set overlap is " + str(round(overp, 2)) + "% -> ABORT")

elif cmp(action, "intersect") == 0:
	# intersect encrypted IP lists
        # order doesn't matter
	fnames = list()
	for i in range(intersect_cnt):
		fnames.append(sys.argv[-intersect_cnt + i])

        (isec_size, sizes) = intersect(fnames)
	for i in range(len(sizes)):
		print "Set", i, "size", sizes[i]
	print "Intersect size", isec_size

	# estimate true intersect if sampled
	if config.has_option("sampling", "sample_rate"):
                data_srate = float(config.get("sampling", "sample_rate"))
		
		isec_est = long(round(float(isec_size) / data_srate))
		serr = long(round(binom_std_err(isec_est, data_srate) / data_srate, 3))
		print "Estimated unsampled intersect size " + str(isec_est) +  "+-" + str(serr)

		# confidence interval
		alpha = 0.05
		cint = binom_cint(isec_est, data_srate, 1-alpha)
		print "Confidence interval " + str(1-alpha) + " " + str(long(cint[0] / data_srate)) + "--" + str(long(cint[1] / data_srate))

else:
	die("Error: unknown action", True)

sys.exit(0)
