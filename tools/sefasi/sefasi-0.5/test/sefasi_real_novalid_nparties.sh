#!/bin/sh
# use sefasi with real datasets without using valid sets (2...N parties)
#
# $Id: sefasi_real_novalid_nparties.sh 715 2013-12-02 01:09:55Z szander $

SPATH=""

if [ $# -lt 4 ] ; then
        echo "Usage: `basename $0` <public_config> <set_cnt> <set1> <set2> [ ... <setN> ] [<use_fast_tools>]"
        exit 1
fi

# public config file
CONFIG=$1

# number os parties/sets
CNT=$2

shift
shift

# set variables for datasets
# SET1=$1, SET2=$2, ...
N=1
while [ ${N} -le ${CNT} ] ; do
	eval SET${N}=\$${N}
	N=`expr ${N} + 1`
done

if [ $# -gt ${CNT} ] ; then
        # use C tools
        FAST="-f"
        echo "Using faster C tools"
fi

N=1
while [ ${N} -le ${CNT} ] ; do 

	# clone the public config
	cp ${CONFIG} sefasi_test_novalid_${N}.pub.cfg

	# generate private config for each party
	echo "GENERATING CONFIG PARTY ${N}"
	${SPATH}sefasi_main.py -a config -c sefasi_test_novalid_${N}.pub.cfg -n sefasi_test_novalid_${N} || exit 1

	# initial encryption and permutation
	echo "INITIAL ENCRYPT&PERMUTE PARTY ${N}"
	eval \${SPATH}sefasi_main.py \${FAST} -a init_enc -c sefasi_test_novalid_\${N}.pub.cfg -p sefasi_test_novalid_\${N}.priv.cfg \${SET${N}} || exit 1

        N=`expr ${N} + 1`
done

N=1
while [ ${N} -le ${CNT} ] ; do

	M=1
	while [ $M -le ${CNT} ] ; do
		if [ ${N} -ne ${M} ] ; then
			echo "PARTY ${N} ENCODES PARTY ${M} DATA"
			eval \${SPATH}sefasi_main.py \${FAST} -a data_enc -c sefasi_test_novalid_\${N}.pub.cfg -p sefasi_test_novalid_\${N}.priv.cfg \${SET${M}}.encperm || exit 1
			# by default each encoding will add an .encperm, but here we
			# keep the same name regardless of number of encodings
			eval mv -f \${SET${M}}.encperm.encperm \${SET${M}}.encperm
		fi

		M=`expr ${M} + 1`
	done

	N=`expr ${N} + 1`
done

# perform the secure set intersection
#${SPATH}sefasi_main.py -f -a intersect -N <number> -c sefasi_test_novalid_1.pub.cfg ${SET1}.encperm ${SET}.encperm ... || exit 1
echo "SECURE SET INTERSECTION"
N=1
CMD="${SPATH}sefasi_main.py ${FAST} -a intersect -N ${CNT} -c sefasi_test_novalid_1.pub.cfg"
while [ ${N} -le ${CNT} ] ; do
	CMD="${CMD} \${SET${N}}.encperm"
	N=`expr ${N} + 1`
done
CMD="$CMD || exit 1"
#echo $CMD
eval $CMD

# perform set intersection on the original datasets
#${SPATH}sefasi_set_intersect -N <number> ${SET1} ${SET2} ... || exit 1
echo -n "TRUE INTERSECT "
N=1
if [ "${FAST}" = "" ] ; then
	CMD="${SPATH}sefasi_set_intersect.py -N ${CNT}"
else
	CMD="${SPATH}sefasi_set_intersect -N ${CNT}"
fi
while [ ${N} -le ${CNT} ] ; do
	# sort the original data, sefasi_set_intersect expects sorted data as input!
	eval cat \${SET${N}} \| LC_ALL\=C sort \> \${SET${N}}.sorted
	CMD="${CMD} \${SET${N}}.sorted"
	N=`expr ${N} + 1`
done
CMD="$CMD || exit 1"
#echo $CMD
eval $CMD
