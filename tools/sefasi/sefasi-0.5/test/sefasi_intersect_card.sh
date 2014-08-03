#!/bin/sh
# compute the set intersection cardinality for the encrypted or raw data (2...N sets)
# including sorting the datasets

CNT=$#

if [ $CNT -lt 2 ] ; then
        echo "Usage: `basename $0` <set1> <set2> [ ... <setN> ]"
        exit 1
fi

# set variables for datasets
# SET1=$1, SET2=$2, ...
N=1
while [ ${N} -le ${CNT} ] ; do
        eval SET${N}=\$${N}
        N=`expr ${N} + 1`
done

# perform set intersection on the original datasets
#${SPATH}sefasi_set_intersect -N <number> ${SET1} ${SET2} ... || exit 1
echo -n "TRUE INTERSECT "
N=1
CMD="${SPATH}sefasi_set_intersect -N ${CNT}"
while [ ${N} -le ${CNT} ] ; do
        # sort the original data, sefasi_set_intersect expects sorted data as input!
        eval cat \${SET${N}} \| LC_ALL\=C sort \> \${SET${N}}.sorted
        CMD="${CMD} \${SET${N}}.sorted"
        N=`expr ${N} + 1`
done
CMD="$CMD || exit 1"
#echo $CMD
eval $CMD
