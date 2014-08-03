#!/bin/sh
# use sefasi with real datasets without using valid sets (2 parties)
#
# $Id: sefasi_real_novalid.sh 714 2013-12-02 01:08:43Z szander $

SPATH=""

CONFIG=$1
SET1=$2
SET2=$3
FAST=$4
if [ "${FAST}" != "" ] ; then
        # use C tools
        FAST="-f"
        echo "Using faster C tools"
fi

if [ "$SET1" == "" -o "$SET2" == "" -o "$CONFIG" == "" ] ; then
        echo "Usage: `basename $0` <public_config> <set1> <set2> [<use_fast_tools>]"
        exit 1
fi

cp ${CONFIG} sefasi_test_novalid_1.pub.cfg
cp ${CONFIG} sefasi_test_novalid_2.pub.cfg
echo "GENERATING CONFIG PARTY 1"
${SPATH}sefasi_main.py -a config -c sefasi_test_novalid_1.pub.cfg -n sefasi_test_novalid_1 || exit 1
echo "GENERATING CONFIG PARTY 2"
${SPATH}sefasi_main.py -a config -c sefasi_test_novalid_2.pub.cfg -n sefasi_test_novalid_2 || exit 1

echo "INITIAL ENCRYPT&PERMUTE PARTY 1"
${SPATH}sefasi_main.py -a init_enc -c sefasi_test_novalid_1.pub.cfg -p sefasi_test_novalid_1.priv.cfg ${SET1} || exit 1 
echo "INITIAL ENCRYPT&PERMUTE PARTY 2"
${SPATH}sefasi_main.py -a init_enc -c sefasi_test_novalid_2.pub.cfg -p sefasi_test_novalid_2.priv.cfg ${SET2} || exit 1

echo "PARTY 1 ENCODES PARTY 2 DATA"
${SPATH}sefasi_main.py -a data_enc -c sefasi_test_novalid_1.pub.cfg -p sefasi_test_novalid_1.priv.cfg ${SET2}.encperm || exit 1
echo "PARTY 2 ENCODES PARTY 1 DATA"
${SPATH}sefasi_main.py -a data_enc -c sefasi_test_novalid_2.pub.cfg -p sefasi_test_novalid_2.priv.cfg ${SET1}.encperm || exit 1

echo "SECURE SET INTERSECTION"
${SPATH}sefasi_main.py -a intersect -c sefasi_test_novalid_1.pub.cfg ${SET1}.encperm.encperm ${SET2}.encperm.encperm || exit 1

cat ${SET1} | LC_ALL=C sort > ${SET1}.sorted
cat ${SET2} | LC_ALL=C sort > ${SET2}.sorted
echo -n "TRUE INTERSECT "
if [ "${FAST}" = "" ] ; then
        ${SPATH}sefasi_set_intersect.py -N 2 ${SET1}.sorted ${SET2}.sorted || exit 1
else
        ${SPATH}sefasi_set_intersect -N 2 ${SET1}.sorted ${SET2}.sorted || exit 1
fi

