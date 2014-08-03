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
# Setup script
#
# $Id: setup.py 864 2014-05-14 02:30:59Z szander $

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'name': 'SeFaSI',
	'description': 'Secure fast set intersection cardinality computation',
	'license': 'GPLv2',
    	'author': 'Sebastian Zander',
	'author_email': 'szander@swin.edu.au',
    	'url': 'http://caia.swin.edu.au/programs/mapping/tools.html',
    	'download_url': 'http://caia.swin.edu.au/programs/mapping/sefasi/sefasi-0.5.tar.gz',
    	'version': '0.5',
    	'install_requires': ['blist >= 1.3.4', 'pycrypto >= 2.6', 'murmur >= 0.1.3'],
    	'packages': [],
    	'scripts': ['src/sefasi_bin2text.py', 'src/sefasi_getcfg.py', 'src/sefasi_sample_items.py', 
		    'src/sefasi_valid_ipset.py', 'src/sefasi_encrypt_items.py', 'src/sefasi_main.py',
		    'src/sefasi_set_intersect.py', 'src/sefasi_text2bin.py', 'src/sefasi_test_ipsets.py',
		    'src/sefasi_capture_data.py']
}

setup(**config)
