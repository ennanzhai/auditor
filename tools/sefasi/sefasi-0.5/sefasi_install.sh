#!/bin/sh
# main install script

PREFIX=$1
if [ "$PREFIX" = "" ] ; then
	PREFIX=/usr/local
fi

echo "-----------------"
echo "Installing SeFaSI"
echo "-----------------"
python setup.py install --prefix=$PREFIX

echo "-------------------------"
echo "Installing SeFaSi C Tools"
echo "-------------------------"
./configure --prefix=$PREFIX
make
make install
