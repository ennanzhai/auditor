SeFaSI version 0.5
------------------

$Id: README.txt 864 2014-05-14 02:30:59Z szander $

OVERVIEW
--------

SeFaSI was developed at the Centre for Advanced Internet Archiectures of 
Swinburne University of Technology as part of the Measuring And Practically 
Predicting INternet Growth (MAPPING) project: http://www.caia.swin.edu.au/mapping .

SeFaSI is a tool that allows multiple parties to securely compute
the set intersection cardinality of IPv4 address data sets while keeping the  
addresses private. SeFaSI works with two or more parties. Note that with set
we mean a mathematical set, which is a collection of _distinct_ objects. 

We developed SeFaSI to use capture-recapture (CR) techniques to estimate the
used IPv4 space when the data sources are private. CR techniques allow to estimate 
a population from multiple incomplete sources. In order to use CR one needs to 
know the sizes of all sources and all sizes of combinations of intersections of 
the sources [1].

However, the underlying technique and a large part of the code is generic
and SeFaSI could be used for other applications, for example in the context of 
social networking. Assume each person has a set of characteristics, such as 
interests or connections. Secure set intersection cardinality allows match-making 
without revealing the characteristics of a person to other people.

SeFaSI is based on commutative encryption. Each participating party first
encrypts and permutes their own data set. Then all other parties encrypt and permute
each other party's encrypted data set. Since the encryption is commutative, the set
intersection cardinality of the n-party encrypted and permuted sets is the
same as the intersection cardinality of the unencrypted sets. Assuming the 
encryption is secure and given that the data sets are permuted by each party, 
no party can learn anything about another party's data set (apart from the
intersection cardinality). This technique is described in more detail in [2,3].

SeFaSI is able to detect probe attacks if the input data is from some known finite 
set [3]. By probe attacks we mean that an attacker constructs a data set with mostly
invalid/impossible items and only a few valid items. Successful probe attacks
allow an attacker to determine if a few specific items are present in other
parties data sets. If a valid set can be specified, SeFaSI can check if other
parties data sets are valid before the actual intersection, and thus it can prevent
probe attacks.  

Another feature of SeFaSI is data sampling [3]. The commutative encryption method
is more efficient than other secure set intersection cardinality computation methods,
but it still has significant computational and storage/transmission costs. SeFaSI
can use deterministic sampling of the data to greatly reduce the input data sets, 
drastically speed up the encryption and drastically reduce the storage/
transmission costs for the encrypted data sets. Large performance gains can be
achieved with relatively small sampling errors. 

Since the size of a union can be expressed in terms of the size of an intersection
and the sizes of the data sets, SeFaSI can also be used to securely compute the size
of a union if the data set sizes are not secret. For example, with two parties
|A v B| = |A| + |B| - |A ^ B|, so the union size can be computed if the sizes of
data sets A and B (|A| and |B|) and the intersection size (|A ^ B|) are known.

Currently, SeFaSI only computes the cardinality of the set intersection
but not the actual set itself.


ALGORITHM AND IMPLEMENTATION DETAILS
------------------------------------

We now describe the algorithm and the implementation in more detail. However,
for a really detailed description please refer to [3].

SeFaSI is implemented in Python. This keeps the source code small and easily
verifiable while ensuring good portability. A drawback of Python is the lower
performance (compared to compiled languages such as C), hence we also 
implemented C versions of some of the performance critical tools.

Our encryption algorithm implementation is based on an RSA implementation.
We use RSA in "commutative mode", that is the modulus components p and q are
public and the encryption exponent e is private. Decryption is not needed and
no decryption exponent is used. This is similar to Pohlig-Hellman encryption 
mentioned in [2,3].

SeFaSI uses config files to store configuration including key material. Each
party must have a public and a private configuration file. The public config
file is shared by all parties while the private config file is unique for each
party and should be kept secret since it contains the encryption key.

We now explain the algorithm step by step.

1) Configuration

All parties agree on a public configuration, which for example specifies 
sample parameters, whether probe detection is used, the public modulus etc. The
easiest approach is to let SeFaSI generate a default public config and then modify
and share this config. With a public config each party can then generate their
own private config.

If probing detection shall be used all parties need to agree on the set of valid
items, for example the routed IPv4 space if the data is observed IPv4
addresses. SeFaSI allows to extract IPv4 data from routing data and can use
sampling to limit the size of the valid data set (referred to as "valid set").

2) Initial encryption

In the initial encryption step each party uses SeFaSI to sample their 
data set (if sampling is used), and then encrypt and permute their data set. 

If probing detection is used each party also samples the valid set, and then
encrypts and permutes their valid set.

Note that the sampling of the data is consistent between all parties. If
an IPv4 address is "in the sample" it will be sampled in the data sets of all parties
that have this address in their unsampled data sets. In contrast, each party selects a
different sample of the valid set (without telling other parties their choice) by
using a private sampling salt.

3) Subsequent valid set encryption

If probing detection is used each party must encrypt and permute each other
party's initially encrypted and permuted valid set. Finally, the valid sets 
encrypted by all parties must be returned to the parties that created them. 

How exactly the valid sets are exchanged is currently left to the parties. 
SeFaSI does not implement a scheme currently. 

At the end of this step each party has their own valid set encrypted and permuted
by all parties.

4) Subsequent data set encryption

Now each party must encrypt and permute each other party's initially
encrypted and permuted data set. In our implementation parties form a ring
structure. Each party receives encrypted data sets from their right neighbour,
encrypt and permute the datasets and pass them on to their left neighbour.

Before a fully encrypted data set is returned to it's creator, it must be
checked for validity if probing detection is used. Each party can use SeFaSI to 
compute the set intersection cardinality between the encrypted data set and the 
valid set. In case of an attempted probing attack the cardinality will be much 
smaller than statistically expected. A party that detects a probing attack 
notifies all other parties.

Finally, all parties send all the fully encrypted data sets to each other or
at least to the parties that are interested in the set intersection cardinality.
Note that no party sends any data sets to a detected probe attacker, so an
attacker cannot compute any intersection cardinality.

At the end of this step all parties that are interested in the set intersection 
cardinality (and did not perform probing attacks) have all data sets encrypted 
and permuted by all parties.

5) Set Intersection cardinality

The final step is the computation of the set intersection cardinalities between 
encrypted data sets. Without data set sampling the results are the same as the 
intersection cardinalities of the original data sets If data set sampling is used, 
SeFaSI computes estimates of the intersection cardinalities as well as confidence 
intervals.


ARCHIVE CONTENTS
----------------

The directory structure is:	

sefasi/.		Makefiles and documentation
sefasi/src		Source code	
sefasi/test		Test/example scripts


CONFIG FILES
------------

Each party that participates needs a public/private configuration pair. The public
configuration specifies sampling parameters, probing detection parameters and
public encryption parameters. The test sub directory contains some example config
files.

Example public config with annotations:
[sampling]
sample_rate= 0.5 	<- sample rate for data
salt= 2573356529	<- sample salt for data 

[probing]
probe_detection= yes 	<- set to yes/no if probing detection should be used/not used
valid_sample_rate= 0.05	<- sample rate of valid set
valid_generate= no 	<- if yes generate valid set, if no use existing valid set
min_data_size= 1000000	<- minimum size of input (sampled) data sets

[encryption]
keylen= 256		<- key length in bits (must be power of 2 and 32 <= keylen <= modlen)
modlen= 256		<- modulus length in bits (must be power of 2 and >= 32)
p= 240392533562968913097477233624108603431	<- p and q are the public modulus
q= 320671053885185848480799823061733369081	   automatically generated


The private config contains the sampling salt for valid data sets and the private
encryption key. Both are automatically generated based on the public config.

Example private config with annotations:
[probing]
valid_salt= 3038911301	<- private sample salt for valid data set
[encryption]
private_key= 60664108018938273705006436868609408115043521529170409238549489718805733807407


The security of SeFaSI depends on the choice of keylen and modlen. NOTE that 
choosing keylen=modlen=256 IS NOT SECURE. We have simply chosen these values for illustrative
purposes and to run the test scripts with higher speed.   

Please consult http://www.keylength.com/ and their references for what is considered secure.

Depending on the application very high security may not be necessary of course.

The min_data_size parameter specifies the minimum size an unsampled data set must have. Small
data sets effectively constitute an probing attack. The choice of the parameter value depends 
on the application and the level of security required.


EXAMPLE USAGE
-------------

SeFaSI consists of a number of separate tools. We now provide some examples
on how to use the tools.

The tool sefasi_main.py ties together the core tools and should
usually be used instead of using the tools directly.

For a number of tools we implemented C versions that run much faster. Using the
-f command line switch with sefasi_main.py will instruct it to use the C tools.
NOTE that the C tools are not 100% compatible with the python tools, for example
sefasi_encrypt_items will not exactly produce the same ciphertexts as 
sefasi_encrypt_items.py due to differences of the used encryption libraries.
IMPORTANT: Consistently use sefasi_main.py with -f or without -f. DO NOT MIX. 

1) Generating config file pairs

The following command generates default public and private config files
test_config.pub.cfg and test_config.priv.cfg:

$ sefasi_main.py -a config -n test_config

The following command generates a private config file given an existing
public config file:

$ sefasi_main.py -a config -c test_config.pub.cfg -n test_config

2) Initial sampling and encryption

The following command samples, encrypts and permutes the data set data_set
containing IPv4 addresses:

$ sefasi_main.py -a init_enc -c sefasi_test.pub.cfg -p sefasi_test.priv.cfg 
data_set

The next command samples, encrypts and permutes the valid set valid_set
and the data set data_set (both containing IPv4 addresses):

$ sefasi_main.py -a init_enc -c sefasi_test.pub.cfg -p sefasi_test.priv.cfg 
valid_set data_set 

3) Subsequent valid set encryption

The following command encrypts and permutes an already encrypted valid set 
valid_set.encperm: 

$ sefasi_main.py -a valid_enc -c sefasi_test.pub.cfg -p sefasi_test.priv.cfg 
valid_set.encperm

4) Subsequent data set encryption

The following command encrypts and permutes an already encrypted data set 
data_set.encperm:

$ sefasi_main.py -a data_enc -c sefasi_test.pub.cfg -p sefasi_test.priv.cfg 
data_set.encperm

The following command encrypts and permutes an already encrypted data set 
data_set.encperm and checks for probing attacks given a valid set encrypted by
all parties valid_set.encperm.encperm (we assume two parties):

$ sefasi_main.py -a data_enc -c sefasi_test.pub.cfg -p sefasi_test.priv.cfg 
valid_set.encperm.encperm data_set.encperm

5) Set intersection

The following command performs the set intersection of two data sets 
encrypted by both parties (we assume two parties):

$ sefasi_main.py -a intersect -c sefasi_test.pub.cfg -N 2 data_set1.encperm.encperm 

The tool sefasi_set_intersect can also be used directly, for example:

$ sefasi_set_intersect.py -N 2 data_set1.encperm.encperm data_set2.encperm.encperm

IMPORTANT: 
The sort action and sefasi_set_intersect assume that the sets are sorted in an order
that uses native byte values. For example, this is the sort order achieved using
the command line tool 'sort' with LC_ALL=C:

$ LC_ALL=C sort data_set1.unordered > data_set1 

If the sets are not sorted the result is likely incorrect!

6) Valid set creation

Instead of creating a valid set as part of "sefasi_main.py -a init_enc" we 
can create a valid set once and use it for multiple set intersections
(assuming the private key remains unchanged).

The following command creates a valid set from routing data routing_snapshot
(e.g. routing snapshot from http://www.routeviews.org/): 

$ cat routing_snapshot | egrep "^\*" | cut -d' ' -f 3 | sefasi_valid_ipset.py -i 0
-r 0.01 -s 1234567890 - > valid_set 

The -r switch is used to specify a sample rate of 0.01 and the chosen salt 
value is 1234567890.

7) Create test IPv4 files

The distribution also contains a little tool to generate some random IPv4
files for testing.

The following command creates two data sets with random IPv4 addresses, the
first data set (data_set_1) has 50000 IPv4s, the second data set (data_set_2)
has 100000 IPv4s, and the intersection cardinality of both data sets is
10000:

$ sefasi_test_ipsets.py -n 50000 -N 100000 -o 10000 -p data_set 

Note, that this tool is only able to generate medium-sized test files but not
very large test files. 

8) Text and binary file conversions

All the core SeFaSI tools work on text files. This is convenient but results in 
some computational and storage overhead. Two tools exist to convert between 
encrypted lists in binary and text format.

The next command converts a text list of encrypted IPs (ips.encperm) into 
binary format (binary file ips_bin.encperm):

$ cat ips.encperm | sefasi_text2bin.py -f 128 -o ips_bin.encperm -

Binary encrypted IPv4s can be converted back to text format using:

$ sefasi_bin2text.py -f 128 -i ips_bin.encperm > ips.encperm 

Note that the -f argument must be used to specify the binary field size in bytes. 
In the example we assume IPs were encrypted as 1024 bits (1024 bits modulus)
which is equivalent to 128 bytes.


TEST SCRIPTS
------------

The test sub directory contains test scripts that also illustrate the
usage of the SeFaSI tools.

The sefasi_test_novalid.sh test script simulates the whole approach for two 
parties without probing detection. The parameters are the sizes of the two
created data sets, the intersection size of the data sets and the public
config file. 

Use the provided example config file sefasi_test_novalid.pub.cfg to
compute the set intersection cardinality without data set sampling or the
example config file sefasi_test_novalid_sample.pub.cfg to compute the set
intersection cardinality with data set sampling (sample rate 0.2).

$ sefasi_test_novalid.sh sefasi_test_novalid_sample.pub.cfg 50000 100000 10000

The sefasi_test.sh test script simulates the whole approach for two parties
using random IPv4 data sets as input. The parameters are the sizes of the two
created data sets, the intersection size of the data sets and the public
config file. 

Use the provided example config file sefasi_test.pub.cfg to 
compute the set intersection cardinality without data set sampling or the
example config file sefasi_test_sample.pub.cfg to compute the set 
intersection cardinality with data set sampling (sample rate 0.2). 

$ sefasi_test.sh sefasi_test_sample.pub.cfg 50000 100000 10000

The sefasi_real_novalid.sh script simulates the whole approach for two
parties without probing detection with real data sets. The parameters are the
names of the two data sets and the public config file.

Use the provided example config file sefasi_test_novalid.pub.cfg to
compute the set intersection cardinality without data set sampling or the
example config file sefasi_test_novalid_sample.pub.cfg to compute the set
intersection cardinality with data set sampling (sample rate 0.2).

$ sefasi_real_novalid.sh sefasi_test_novalid_sample.pub.cfg dataset1 dataset2

To run the scripts sefasi_test.sh, sefasi_test_novalid.sh, or sefasi_real_novalid.sh 
with the faster C tools instead of the slower Python tools set the last optional 
parameter to any value (e.g. 'Y'):

$ sefasi_test_novalid.sh sefasi_test_novalid_sample.pub.cfg 50000 100000 10000 Y
$ sefasi_real_novalid.sh sefasi_test_novalid_sample.pub.cfg dataset1 dataset2 Y

The script sefasi_real_novalid_nparties.sh is a version of sefasi_real_novalid.sh 
that works for 2...N parties/datasets. For example, the following command computes
the intersection cardinality for the datasets of three parties:

$ sefasi_real_novalid_nparties.sh sefasi_test_novalid_sample.pub.cfg 3 dataset1 dataset2 dataset3

Or we can do the same using the faster C tools:

$ sefasi_real_novalid_nparties.sh sefasi_test_novalid_sample.pub.cfg 3 dataset1 dataset2 dataset3 Y


AUTOMATING THE PROCESS WITH MULTIPLE PARTIES
--------------------------------------------

The script sefasi_peer.sh allows to automate the set intersection process
in the case of multiple distributed parties. However, the initial configuration
steps need to be done by hand.

1. All parties need to agree on the list of participating hosts (peers)
   and their hostnames or IP addresses. The list of addresses/names is viewed as ring. 
   Data sets other than the fully-encrypted data sets are only passed to the left neighbour
   which is the name/address before the name/address of the local peer in the list. 
   For example, assume we have the list "192.168.1.1 192.168.1.2 192.168.1.3".
   The left neighbour of 192.168.1.1 is 192.168.1.3, the left neighbour of 
   192.168.1.2 is 192.168.1.1 and so on.

2. Each party must create two user accounts on their host (or one account if an existing 
   account can be used. Each party must create a user "sefasi". This user must not
   have access to the private unencrypted data sets or the private configuration
   file that contains the encryption key. This user account is used for other parties
   to upload data. The second (possibly existing) user account is used to run sefasi_peer.sh
   and must have access to the unencrypted dataset and the private sefasi configuration.

   In the following we refer to these two accounts as the "sefasi" acccout and the
   "main" account.

   File permissions in the "sefasi" account must be set such that the other
   user account can read files (e.g. by setting umask 022 in the shell configuration).
   On many systems this will be the default permissions.

   File permissions for the "main" account must be set such that the "sefasi"
   account has no access to the unencrypted dataset and the private sefasi configuration.
   By default the generated private configuration is only readable for the owner.

3. Each party must generate an RSA key pair for the "main" account for use with SSH. For
   example, by running the following command and RSA key pair is created:

   $ ssh-keygen -t rsa

   The private key (id_rsa) and public key (id_rsa.pub) files are placed in the 
   HOME/.ssh directory, where HOME is the home directory of the "main" account.

   If a key pair already exists it can be used.

   Note that sefasi_peer.sh currently only uses the default key pair (id_rsa, id_rsa.pub).
   There is no support to use particular key pairs with non-default names yet. 

4. Each party must add all parties public RSA keys (generated in the last step) to their
   ~sefasi/.ssh/authorized_keys file _including_ their own public RSA key. This means 
   each party must send their generated id_rsa.pub file to all other parties.

5. All parties must agree on the _public_ SeFaSI configuration to be used. Based on 
   the agreed public configuration all parties must generate their private SeFaSI keys.
   The configuration should be stored in a directory of the "main" user. 
   For example, a directory can be setup as follows.
 
   $ mkdir /home/someuser/sefasi
   $ cp test.pub.cfg /home/someuser/sefasi
   $ cd /home/someuser/sefasi
   $ sefasi_get_cfg.py -c test.pub.cfg

   The sefasi_get_cfg.py command will generate the file test.priv.cfg in /home/someuser/sefasi.
   The directory /home/someuser/sefasi then needs to be specified as PREFIX when
   starting sefasi_peer.sh (see setp 7).

6. Each party must perform the initial sampling and encryption of their dataset.
   For example, if the dataset is data.txt the following command can be used:

   $ sefasi_main.py -f -a init_enc -c test.pub.cfg -p test.priv.cfg data.txt 

   This command will generate the files data.txt.encperm (encrypted and permuted
   dataset) and data.txt.size (contains the true size of the dataset).

7. Each party then can start sefasi_peer.sh. For example, if the peer list is
   "192.168.1.1 192.168.1.2 192.168.1.3", the local IP is 192.168.1.2, and the directory 
   PREFIX to be used is /home/someuser/sefasi, the command is:

   $ sefasi_peer.sh test.pub.cfg test.priv.cfg "192.168.1.1 192.168.1.2 
   	192.168.1.3" 192.168.1.2 /home/someuser/sefasi

   sefasi_peer.sh will check the reachability of all peers with ssh, create working
   directories below PREFIX and then wait for the user to put the .encperm and .size 
   files generated in step 6 into the appropriate directory (by default PREFIX/own). The
   files can also be copied into this directory before starting sefasi_peer.sh.

   sefasi_peer.sh will pass the encrypted and permuted local dataset to the left
   neighbour. Once an encrypted dataset is received from the right neighbour 
   sefasi_peer.sh will encrypt and permute the dataset and pass it to the left neighbour. 
   The process will continue until all data sets have been encrypted by all peers. Fully
   encrypted data sets will then be send to all peers. After all fully encrypted data sets
   have been received sefasi_peer.sh will compute the intersection cardinalities
   between all data sets.

Note that sefasi_peer.sh creates three directories under PREFIX. PREFIX/own is where the
local encrypted dataset and the corresponding size file need to be put. PREFIX/work is used 
to store all files received and all files created. PREFIX/final contains all fully-encrypted 
datasets after sefasi_peer.sh terminates.

Note that peers copy data sets to their left neighbours inbox directory (by default 
/home/sefasi/sefasi_inbox) using scp. The user that holds the inbox can be changed via
the command line -- a list of user names can be specified as last command line parameter
when starting sefasi_peer.sh (after the PREFIX). This feature is mainly for testing where
it is convenient to use only one user account. However, this approach is insecure and 
should be used for testing only.

For example, we can specify that the someuser account will be used to hold the inbox
and run sefasi_peer.sh. Again, this is insecure and should be used for testing only.

$ sefasi_peer.sh test.pub.cfg test.priv.cfg "192.168.1.1 192.168.1.2
     192.168.1.3" 192.168.1.2 /home/someuser/sefasi "someuser someuser someuser"

Note that sefasi_peer.sh will create the inbox directory of the left neighbour if it 
doesn't exist.

Note that sefasi_peer.sh currently does not support probing detection.
 

OTHER APPLICATIONS
------------------

SeFaSI was developed with IPv4 address data in mind but it can be used with 
other data sets. Only the valid set creation (sefasi_valid_ipset.py) and test set 
creation (sefasi_test_ipsets.py) scripts are specific to IPv4 address data. 


COPYRIGHT
---------

Copyright (c) 2013 Centre for Advanced Internet Architectures,
Swinburne University of Technology.

Author: Sebastian Zander (szander@swin.edu.au)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as 
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

Note that the Python modules SeFaSI uses are copyrighted under their own
respective licenses: basic Python modules (Python license), blist (3-clause BSD),
PyCrypto (public domain license), Murmur (MIT license).

Note that the ini file reader and murmur hash code used by the C tools
have their own licenses: ini reader (3-clause BSD), murmur (no copyright).


ACKNOWLEDGEMENTS
----------------

This tool has been made possible in part by an Australian Research Council (ARC)
Linkage Project grant (project LP110100240) with APNIC Pty Ltd as partner 
organisation, for a project titled "Tools and models for measuring and predicting 
growth in internet addressing and routing complexity".


REFERENCES
----------

[1]  S. Zander, L. L. H. Andrew, G. Armitage, G. Huston, "Estimating IPv4 Address 
     Space Usage with Capture-Recapture", (accepted at) 7th IEEE Workshop on 
     Network Measurements (WNM) in conjunction with the 38th IEEE Conference 
     on Local Computer Networks (LCN), Sydney, Australia, October 2013. 

[2]  J. Vaidya, C. Clifton, "Secure Set Intersection Cardinality with Application
     to Association Rule Mining", J. Comput. Secur., vol. 13, pp. 593--622,
     July 2005. 

[3]  S. Zander, L. L. H. Andrew, G. Armitage, "Scalable Private Set Intersection
     Cardinality for Capture-Recapture with Multiple Private Datasets", Tech. Rep. 
     130930A, Centre for Advanced Internet Architectures, Swinburne University of 
     Technology, 2013.


CONTACT
-------

If you have any questions or want to report any bugs please contact
Sebastian Zander (szander@swin.edu.au).

Centre for Advanced Internet Architectures
Swinburne University of Technology
Melbourne, Australia
CRICOS number 00111D
http://www.caia.swin.edu.au

