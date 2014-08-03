#!/bin/sh
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
# sefasi peer process, run on each peer participating in the set intersection 
# prerequisites: see README 
# TODO: handle stalled scp connections better
#       currently we can only kill the scp process and sefasi_peer.sh should resume
#
# $Id: sefasi_peer.sh 710 2013-11-25 03:55:29Z szander $


mymove() {
	# param 1: source file
	# param 2: destination file 
	if [ "$INBOX_USER" = "$USER" ] ; then
        	mv $1 $2
        else
        	cp -p $1 $2
                ssh -q $INBOX_USER@localhost "rm -f $1"
        fi
}

myremove() {
	# param 1: file 
        if [ "$INBOX_USER" = "$USER" ] ; then
                rm -f $1
        else
                ssh -q $INBOX_USER@localhost "rm -f $1"
        fi
}

myfstat() {
	# param 1: file
	if [ "$INBOX_USER" = "$USER" ] ; then
        	ACTIVE=`$FILE_STAT $1 | grep -v "USER" | wc -l | awk '{ print $1 }'`
        else
        	ACTIVE=`ssh -q $INBOX_USER@localhost $FILE_STAT $1 | grep -v "USER" | wc -l | awk '{ print $1 }'`   
        fi

	echo $ACTIVE
}

mywaitrecv() {
	# param 1: file
	while [ 1 ] ; do
         	ACTIVE=`myfstat $1`
                if [ $ACTIVE -eq 0 ] ; then
                	break
                fi
                sleep 1
        done
}

mysendfile() {
	# param 1: file name
	# param 2: user@host:path
	echo "scp $1 $2"
	# send md5sum as file first
	$FILE_MD5 $1 | cut -d'=' -f 2 | awk '{ print $1 }' > ${1}.md5
	while [ 1 ] ; do
		scp ${1}.md5 $2 
		if [ $? -eq 0 ] ; then
                	break
                fi
                sleep 1
        done
	rm -f ${1}.md5
	# send file
        while [ 1 ] ; do
        	scp $1 $2
                if [ $? -eq 0 ] ; then
                	break
                fi
                sleep 1
        done
}


# configuration
SEFASI_PUB_CFG=$1
SEFASI_PRIV_CFG=$2
# list of all peers
PEERS=$3
# local peer address
LOCAL_PEER=$4
# path prefix
PREFIX=$5
if [ "$PREFIX" = "" ] ; then
	PREFIX="/home/`echo $USER`/sefasi"
fi
# inbox user 
INBOX_USER="sefasi"
# public inbox dir into which other peers upload datasets (XXX not configurable at the moment)
INBOX_DIR="sefasi_inbox"
# private directories
# directory for own encrypted file 
OWN="${PREFIX}/own"
# working directory (can be different for each peer)
WORK="${PREFIX}/work"
# final fully encrypted datasets (can be different for each peer)
FINAL="${PREFIX}/final"
INBOX_USER_LIST=$6
if [ "$INBOX_USER_LIST" = "" ] ; then
	for P in $PEERS ; do
		if [ "$INBOX_USER_LIST" = "" ] ; then
			INBOX_USER_LIST="$INBOX_USER"
		else
        		INBOX_USER_LIST="$INBOX_USER_LIST $INBOX_USER"
		fi
	done
fi

# check arguments
if [ $# -lt 4 -o $# -gt 6 ] ; then
        echo "Usage: `basename $0` <public_cfg> <private_cfg> <peer_list> <local_peer> [<dir_prefix>] [<inbox_users>]"
        echo "          <public_cfg>    	Public SeFaSI configuration to be used"
        echo "          <private_cfg>   	Private SeFaSI configuration to be used"
        echo "          <peer_list>     	List of peers (IPs or hostnames) in double-quotes separated by spaces"
        echo "          <local_peer>    	Local peer (IP or hostname)"
        echo "          <dir_prefix>    	Path prefix under which the working directories are (default is $PREFIX)"
        echo "          <inbox_users>   	List of inbox users for peers in double-quotes separated by spaces (default is all are $INBOX_USER)"
        exit 1
fi

# check if config files are there
if [ ! -f $SEFASI_PUB_CFG ] ; then
        echo "Error: can't access public config file '$SEFASI_PUB_CFG'"
        exit 1
fi
if [ ! -f $SEFASI_PRIV_CFG ] ; then
	echo "Error: can't access private config file '$SEFASI_PRIV_CFG'"
	exit 1
fi

# secure private config
chmod 600 $SEFASI_PRIV_CFG

# check for essential tools

# file stats checker
if [ "`which lsof`" != "" ] ; then
	FILE_STAT=lsof
elif [ "`which fstat`" != "" ] ; then
	FILE_STAT=fstat
else
	echo "Error: need installed lsof or fstat, aborting"
	exit 1
fi
# md5 tool checker
if [ "`which md5sum`" != "" ] ; then
        FILE_MD5=md5sum
elif [ "`which md5`" != "" ] ; then
        FILE_MD5=md5
else
        echo "Error: need installed md5sum or md5, aborting"
        exit 1
fi

# peer to send data to
NEXT_PEER=""
# next peers inbox
NEXT_PEER_INBOX=""
# number of peers
PEERS_CNT=0

# dirty trick, use this so we can access any element of inbox list using: eval ARG='$'{$I} 
# don't need to save original command line arguments
set -- $INBOX_USER_LIST

echo "Checking peers..."

# check if all other peers are up and ssh works
# if not abort
CNT=1
for P in $PEERS ; do
	eval ARG='$'{$CNT}
	if [ "$P" != "$LOCAL_PEER" ] ; then
		#echo "ssh -q -o ConnectTimeout=3 ${ARG}@${P} exit"
		ssh -q -o ConnectTimeout=3 ${ARG}@${P} exit
		if [ $? -eq 0 ] ; then
			echo "Peer ${ARG}@${P} is working"
		else
			echo "Peer ${ARG}@${P} is not working, aborting"
			exit 1
		fi
	fi	
	CNT=`expr $CNT + 1`	
	PEERS_CNT=`expr $PEERS_CNT + 1`	
done

# setup inbox dir and find our left neighbour (we will send data to)
LAST=""
CNT=1
for P in $PEERS ; do
	eval ARG='$'{$CNT}
	if [ "$P" = "$LOCAL_PEER" ] ; then
		# setup left neighbour 
		NEXT_PEER=$LAST
        	NEXT_PEER_INBOX_USER=$LAST_USER
        	NEXT_PEER_INBOX="/home/$NEXT_PEER_INBOX_USER/$INBOX_DIR"
		# set our own inbox user
                INBOX_USER=$ARG
		INBOX="/home/$INBOX_USER/$INBOX_DIR"
	fi
	LAST=$P
	LAST_USER=$ARG
	CNT=`expr $CNT + 1`
done
if [ "$NEXT_PEER" = "" ] ; then
	NEXT_PEER=$LAST
	NEXT_PEER_INBOX_USER=$LAST_USER
	NEXT_PEER_INBOX="/home/$NEXT_PEER_INBOX_USER/$INBOX_DIR"
fi

echo "Checking inbox account..."

if [ "$INBOX_USER" != "$USER" ] ; then
        #echo ssh -q -o ConnectTimeout=3 ${ARG}@localhost exit
        ssh -q -o ConnectTimeout=3 ${INBOX_USER}@localhost exit
        if [ $? -eq 0 ] ; then
                echo "Access to ${INBOX_USER}@localhost is working"
        else
                echo "Access to ${INBOX_USER}@localhost is not working, aborting"
		exit 1
        fi
else
        echo "WARNING: same user account used for inbox, this is INSECURE"
fi

# create inbox directory at peer (if not exists)
echo "Next peer is ${NEXT_PEER_INBOX_USER}@${NEXT_PEER} (inbox $NEXT_PEER_INBOX)"
echo "Creating inbox on next peer..."
ssh -q -o ConnectTimeout=3 ${NEXT_PEER_INBOX_USER}@${NEXT_PEER} "mkdir -p $NEXT_PEER_INBOX"
#echo ""

echo "Cleaning directory $WORK"
echo "Cleaning directory $FINAL"
echo ""
#echo "Press any key to continue..."
#read DUMMY

# create directories
mkdir -p $OWN
mkdir -p $WORK
mkdir -p $FINAL

# remove stale files 
rm -f ${WORK}/*
rm -f ${FINAL}/*

# set restrictive permissions
chmod 700 $PREFIX
chmod 700 $OWN 
chmod 700 $WORK 
chmod 700 $FINAL 
find $PREFIX -maxdepth 0 -type f -exec chmod 600 '{}' \;

# make sure we have local encrypted dataset 
echo "Before continuing make sure you have done the initial dataset sampling and encryption, e.g. with"
echo "sefasi_main.py -f -a init_enc -c $SEFASI_PUB_CFG -p $SEFASI_PRIV_CFG <data_file> ,"
echo "and you have copied the resulting .encperm and .size files to ${OWN}!"
echo "Press any key to continue..."
read DUMMY

# check that we have exactly one .encperm and one .size
echo "Forwarding own enrypted dataset"
TEST1=`find $OWN -type f -name "*.encperm" -print | wc -l | awk '{ print $1 }'`
TEST2=`find $OWN -type f -name "*.size" -print | wc -l | awk '{ print $1 }'`
TEST3=`find $OWN -type f -print | wc -l | awk '{ print $1 }'`
if [ $TEST1 -ne 1 -o $TEST2 -ne 1 -o $TEST3 -gt 2 ] ; then
	echo "Error: $OWN must contain exactly one .encperm and one .size file" 
        exit 1
fi

while [ 1 ] ; do
        FILE=`find $OWN -type f -print | sort -r | head -1`
	if [ "$FILE" = "" ] ; then
		break
	fi
	mysendfile $FILE ${NEXT_PEER_INBOX_USER}@${NEXT_PEER}:${NEXT_PEER_INBOX}
	mv $FILE $WORK
done

echo ""

echo "Entering loop (own inbox $INBOX)"

CNT=1
while [ 1 ] ; do
	# check if data files in inbox
	# sort ensures that the .size files are always found before the .encperm files
	FILE=`find $INBOX -type f \! -name "*.md5" -print | sort -r | head -1`
	# if yes wait until file is there completely (check with lsof or fstat (FreeBSD) if file is still written)
	if [ "$FILE" != "" ] ; then
	        echo "New file detected $FILE"
		mywaitrecv $FILE
                echo "New file complete $FILE"

		# check if file received is OK
		if [ ! -f ${FILE}.md5 ] ; then
			echo "No MD5 $FILE"
			myremove $FILE	
			continue
		fi
		MD5=`$FILE_MD5 $FILE | cut -d'=' -f 2 | awk '{ print $1 }'`
		if [ "$MD5" != "`cat ${FILE}.md5`" ] ; then
			echo "Wrong MD5 $FILE"
			myremove $FILE
			myremove ${FILE}.md5
			continue
		else	
			echo "Correct MD5 $FILE"
			myremove ${FILE}.md5
		fi

		if [ "`echo $FILE | sed -e "s/.*\.//"`" = "size" ] ; then
                        # move size files straight to work directory and continue
			mymove $FILE $WORK
			echo "Moved to work dir $FILE"
                        continue
                fi

		if [ $CNT -ge $PEERS_CNT ] ; then
			# move fully encrypted datasets to work and final
			cp $FILE $WORK
			mymove $FILE $FINAL
			echo "Moved to work and final dirs $FILE"

			CNT=`expr $CNT + 1`
			
			if [ $CNT -eq `expr $PEERS_CNT \* 2 - 1` ] ; then
				#stop if we have all fully encrypted datasets
				break
			fi
			continue
		fi

		mymove $FILE $WORK
		FILE=$WORK/`basename $FILE`
		echo "Moved to work dir $FILE"

		# encrypt and permute
		echo "sefasi_main.py -f -a data_enc -c $SEFASI_PUB_CFG -p $SEFASI_PRIV_CFG $FILE"
		sefasi_main.py -f -a data_enc -c $SEFASI_PUB_CFG -p $SEFASI_PRIV_CFG $FILE

		if [ $? -ne 0 ] ; then
			# abort
			echo "ABORT"
			exit 1
		fi

		# increase counter
		CNT=`expr $CNT + 1` 

		if [ $CNT -eq $PEERS_CNT ] ; then
			# if CNT equals number of peers broadcast fully encrypted dataset and exit
			CNT2=1
			for P in $PEERS ; do
        			if [ "$P" != "$LOCAL_PEER" ] ; then
					eval ARG='$'{$CNT2}
                			P_INBOX_USER=$ARG
					P_INBOX="/home/$P_INBOX_USER/$INBOX_DIR"
					mysendfile $FILE.encperm ${P_INBOX_USER}@${P}:${P_INBOX}
				fi
				CNT2=`expr $CNT2 + 1`
			done
			cp $FILE.encperm $FINAL
		else
			# scp encrypted and permuted file and related .size file to NEXT_PEER
			SIZE_FILE=`echo $FILE | sed 's/\.encperm$/.size/' | sed 's/\.encperm//g'`
			mysendfile ${SIZE_FILE} ${NEXT_PEER_INBOX_USER}@${NEXT_PEER}:${NEXT_PEER_INBOX}
			mysendfile $FILE.encperm ${NEXT_PEER_INBOX_USER}@${NEXT_PEER}:${NEXT_PEER_INBOX}
		fi
	fi

	sleep 1
done

echo "Computing all intersections"
SRATE=`cat $SEFASI_PUB_CFG | egrep "^sample_rate" | awk '{ print $2 }'`
echo "Sample rate $SRATE"
FILES=`find $FINAL -type f -print | sort`
echo -n "Datasets "
for F in $FILES ; do
	echo -n "`basename $F | sed -e "s/\.encperm//g"` "
done
echo ""
sefasi_capture_data -r $SRATE -N $PEERS_CNT $FILES 

echo "Cleaning our inbox"
myremove ${INBOX}/* 
echo "Done"
