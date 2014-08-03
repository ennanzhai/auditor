#!/bin/sh
# test sefasi with test datasets without using valid sets (2 parties)
#
# $Id: sefasi_test_novalid.sh 714 2013-12-02 01:08:43Z szander $

SPATH=""
SET_NAME_PFX="testset"

CONFIG=$1
SET1_SIZE=$2
SET2_SIZE=$3
OVERLAP=$4
FAST=$5
if [ "${FAST}" != "" ] ; then
        # use C tools
        FAST="-f"
        echo "Using faster C tools"
fi

if [ "$SET1_SIZE" == "" -o "$SET2_SIZE" == "" -o "OVERLAP" == "" -o "$CONFIG" == "" ] ; then
        echo "Usage: `basename $0` <public_config> <set1_size> <set2_size> <overlap_size> [<use_fast_tools>]"
        exit 1
fi

echo "GENERATING TEST DATASETS"
${SPATH}sefasi_test_ipsets.py -n ${SET1_SIZE} -N ${SET2_SIZE} -o ${OVERLAP} -p ${SET_NAME_PFX} || exit 1 

cp ${CONFIG} sefasi_test_novalid_1.pub.cfg
cp ${CONFIG} sefasi_test_novalid_2.pub.cfg
echo "GENERATING CONFIG PARTY 1"
${SPATH}sefasi_main.py -a config -c sefasi_test_novalid_1.pub.cfg -n sefasi_test_novalid_1 || exit 1
echo "GENERATING CONFIG PARTY 2"
${SPATH}sefasi_main.py -a config -c sefasi_test_novalid_2.pub.cfg -n sefasi_test_novalid_2 || exit 1

echo "INITIAL ENCRYPT&PERMUTE PARTY 1"
${SPATH}sefasi_main.py ${FAST} -a init_enc -c sefasi_test_novalid_1.pub.cfg -p sefasi_test_novalid_1.priv.cfg ${SET_NAME_PFX}_1 || exit 1 
echo "INITIAL ENCRYPT&PERMUTE PARTY 2"
${SPATH}sefasi_main.py ${FAST} -a init_enc -c sefasi_test_novalid_2.pub.cfg -p sefasi_test_novalid_2.priv.cfg ${SET_NAME_PFX}_2 || exit 1

echo "PARTY 1 ENCODES PARTY 2 DATA"
${SPATH}sefasi_main.py ${FAST} -a data_enc -c sefasi_test_novalid_1.pub.cfg -p sefasi_test_novalid_1.priv.cfg ${SET_NAME_PFX}_2.encperm || exit 1
echo "PARTY 2 ENCODES PARTY 1 DATA"
${SPATH}sefasi_main.py ${FAST} -a data_enc -c sefasi_test_novalid_2.pub.cfg -p sefasi_test_novalid_2.priv.cfg ${SET_NAME_PFX}_1.encperm || exit 1

echo "SECURE SET INTERSECTION"
${SPATH}sefasi_main.py -a intersect -c sefasi_test_novalid_1.pub.cfg ${SET_NAME_PFX}_1.encperm.encperm ${SET_NAME_PFX}_2.encperm.encperm || exit 1
echo -n "TRUE INTERSECT "
if [ "${FAST}" = "" ] ; then
        ${SPATH}sefasi_set_intersect.py -N 2 ${SET_NAME_PFX}_1 ${SET_NAME_PFX}_2 || exit 1
else
        ${SPATH}sefasi_set_intersect -N 2 ${SET_NAME_PFX}_1 ${SET_NAME_PFX}_2 || exit 1
fi

