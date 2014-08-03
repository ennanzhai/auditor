/*
    Copyright (c) 2011-2012 Centre for Advanced Internet Architectures,
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

    sefasi_sample_items.cc
    Sample item using deterministic sampling

    $Id: sefasi_sample_items.cc 864 2014-05-14 02:30:59Z szander $
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <getopt.h>
#include <string.h>
#include <math.h>
#include <err.h>
#include <errno.h>
#include <sysexits.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <string>

#include "sefasi_common.h"
#include "murmur3.h"

using namespace std;



// all the hash names
typedef enum
{
	sha1 = 0,
	md5,
	murmur
} hash_names_t;	

// globals

// verbosity level
int verbose = 0;


inline __attribute__((always_inline)) uint32_t hash_val(hash_names_t hf, const void * key, int len, uint64_t salt)
{
	uint32_t ret;

	switch (hf) {
		case sha1:
			return 0;
		case md5:
			return 0;
		case murmur:
			// we just pass the salt as seed for performance reasons
			MurmurHash3_x86_32(key, len, (uint32_t) salt, &ret);
			//MurmurHash3_x64_128(key, len, salt, &ret);
			return ret;

		default:
			return 0;
	}
}


// print usage
void usage(char *name)
{

	cout << "Usage: " << name << " [OPTIONS] <-|item_list> " << endl;
	cout << "       -h                                      show usage" << endl;
	cout << "       -H <hash_function>         		hash function to be used ('sha1' or 'md5' or 'murmur', default 'murmur')" << endl;
	cout << "       -i <index>         			index of input file that contains IP addresses" << endl;
	cout << "       -r <sample_rate>         		sample rate that must be 1.0 or equal smaller 0.5 (default 1.0)" << endl;
	cout << "       -s <salt>         			random 'salt' that is xored with IP before hashing (default 0)" << endl;
	cout << "       -v       				enable verbose mode" << endl;
	cout << "       <-|item_list>      			file name to read item from or '-' to read from stdin" << endl;

}


int main(int argc, char **argv)
{
	int c;
	char *endptr;
	opterr = 0;
	FILE *item_file;

	hash_names_t hash = murmur;
	unsigned int idx = 0;
	//double sample_rate = 1.0;
	unsigned int sample_mod = 1;
	uint64_t salt = 0;

	//srand48(time(NULL));
	//srandom(time(NULL));

	while ((c = getopt(argc, argv, "hH:i:Ir:s:v")) != -1) {
		switch (c)
		{
			case 'H':
				if (strcasecmp(optarg, "sha1") == 0) {
					errx(EX_USAGE, "Error: SHA1 hash function not implemented yet");	
				} else if (strcasecmp(optarg, "md5") == 0) {
					errx(EX_USAGE, "Error: MD5 hash function not implemented yet");
				} else if (strcasecmp(optarg, "murmur") == 0) {
					hash = murmur;
				} else {
					errx(EX_USAGE, "Error: hash function '%s' not implemented", optarg);
				}
				break;

			case 'i':
				{
                                        unsigned long x = strtoul(optarg, &endptr, 10);
                                        if (*endptr) {
                                                errx(EX_USAGE, "Error: parsing index value '%s'", endptr);
                                        }

					idx = x;
                                }
                                break;

			case 'I':
				break;

			case 'r':
				{
					double x = strtod(optarg, &endptr);
					if (*endptr) {
						errx(EX_USAGE, "Error: parsing sample rate '%s'", endptr);
					}

					if (x < 0.0 || x > 1.0) {
						errx(EX_USAGE, "Error: sample rate must be between 0.0 and 1.0");
					}

					// XXX check on whether the inverse is an integer

					sample_mod = (unsigned int) round(1.0 / x);
					//sample_rate = x;

				}
				break;

			case 's':
                                {
                                        unsigned long long x = strtoull(optarg, &endptr, 10);
                                        if (*endptr) {
                                                errx(EX_USAGE, "Error: parsing salt value '%s'", endptr);
                                        }

                                        salt = x;
                                }
                                break;


			case 'h':
				usage(argv[0]);
				exit(0);
				break;

			case 'v':
				verbose = 1;
				break;

			case '?':
			default:
				usage(argv[0]);
				exit(1);
		}
	}

	// open file or stdin

	if (optind < argc) {
		if (strcmp(argv[optind], "-") == 0) {
			item_file = stdin;
		} else {
                	item_file = fopen(argv[optind], "r");
                	if (item_file == NULL) {
				errx(EX_USAGE, "Error: can't open item file '%s'", argv[optind]);
                	}
		}
        } else {
                usage(argv[0]);
                exit(1);
        }

	// processing loop

	char s1[MAX_ITEM_LEN+1];
	unsigned long line = 0;
	while (fscanf(item_file, "%"xstr(MAX_ITEM_LEN)"[^\n]\n", (char*)&s1) != EOF) {
		unsigned int i = 0;
		uint32_t h = 0;
		char *field = NULL;
		char *p = s1;

		while (i <= idx) {
			field = strsep(&p, " ");	
			if (field == NULL) {
				errx(EX_DATAERR, "Error: line %ld has fewer than %u elements", line, idx);	
			}
			i++;
		}
		// replace end of line 
		p = strstr(field, "\n");
               	if (p != NULL) {
                       	*p = '\0';
		}

		h = hash_val(hash, field, strlen(field), salt);
		if (h % sample_mod == 0) {
			printf("%s\n", field);
		}
		
		line++;
	}

	fclose(item_file);

	return 0;
}

