# apt-rdepends, version 1.3.0
#
# apt-rdepends performs recursive dependency listings similar to apt-cache.
# Copyright (C) 2002  Simon Law
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

VERSION=1.3.0

SHELL = /bin/sh

prefix = /usr/local
exec_prefix = ${prefix}

bindir = ${exec_prefix}/bin
mandir = ${prefix}/share/man

INSTALL = /usr/bin/install -c
INSTALL_DATA = ${INSTALL} -m 644

all : apt-rdepends.8

apt-rdepends.8 : apt-rdepends
	pod2man --section=8 --release=${VERSION} --center=" " $< > $@

install :
	mkdir -p ${bindir}; \
	${INSTALL} apt-rdepends ${bindir}; \

install-man : all
	mkdir -p ${mandir}/man8; \
	${INSTALL_DATA} apt-rdepends.8 ${mandir}/man8;

clean :
	rm -f apt-rdepends.8

.PHONY : all install clean
