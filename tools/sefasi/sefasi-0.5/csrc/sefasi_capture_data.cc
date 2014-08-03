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

    sefasi_capture_data.cc
    Get capture count table (compute set intersections) 

    $Id: sefasi_capture_data.cc 710 2013-11-25 03:55:29Z szander $
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

using namespace std;


// globals

// number of sources
unsigned int sources_cnt = 2;

// file descriptors for each source
FILE *sources[MAX_SOURCES];

// verbosity level
int verbose = 0;


// print usage
void usage(char *name)
{

	cout << "Usage: " << name << " [OPTIONS] <source1> <source2> ... <sourceN> " << endl;
	cout << "       -h                                      show usage" << endl;
	cout << "       -i <index>         			index of input file that contains IP addresses" << endl;
	cout << "       -N <sources_cnt>         		number of input files (must be at least 2)" << endl;
	cout << "       -o <out_file>         			if specified the intersect set will be written to file" << endl;
	cout << "       -r <sample_rate>         		sample rate of the input data (default 1.0)" << endl;
	cout << "       -v       				enable verbose mode" << endl;
	cout << "       <source1> <source2>      		(encrypted) item lists (data sources)" << endl;

}


int keep_going(int ends[])
{
        unsigned int i;

        for (i=0; i<sources_cnt; i++) {
                if (ends[i] == 0) {
                        return 1;
                }
        }

        return 0;
}


static int cmpstringp(const void *p1, const void *p2)
{
	return strcmp(*((const char **) p1), *((const char **) p2));
}



int main(int argc, char **argv)
{
	int c;
	unsigned int i, j, cnt;
	char *endptr;
	opterr = 0;

	unsigned int idx = 0;
	string out_fname = "";

	unsigned long long *counters;
	unsigned int rows = 0;
	double sample_rate = 1.0;

	//srand48(time(NULL));
	//srandom(time(NULL));

	while ((c = getopt(argc, argv, "hi:N:o:r:v")) != -1) {
		switch (c)
		{
			case 'i':
				{
                                        unsigned long x = strtoul(optarg, &endptr, 10);
                                        if (*endptr) {
                                                errx(EX_USAGE, "Error: parsing index value '%s'", endptr);
                                        }

					idx = x;
                                }
                                break;

			case 'N':
				{
                                        unsigned long x = strtoul(optarg, &endptr, 10);
                                        if (*endptr) {
                                                errx(EX_USAGE, "Error: parsing number of sources value '%s'", endptr);
                                        }

					if (x < 2 || x > MAX_SOURCES) {
						errx(EX_USAGE, "Error: number of sources must be between 2 and %d", MAX_SOURCES);
					}

                                        sources_cnt = x;
                                }
                                break;

			case 'o':
				out_fname = string(optarg);
                                break;

			case 'r':
                                {
                                        double x = strtod(optarg, &endptr);
                                        if (*endptr) {
                                                errx(EX_USAGE, "Error: parsing sample rate value '%s'", endptr);
                                        }

                                        if (x < 0.0 || x > 0.5) {
                                                errx(EX_USAGE, "Error: sample rate must be between 0.0 and 0.5");
                                        }

                                        sample_rate = x;
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

	// allocate counters list (XXX we allocate the all zero row that is never used)
	rows = pow(2, sources_cnt);
	counters = (unsigned long long *) calloc(rows, sizeof(unsigned long long));

	// open source files
	for (i=0; i<sources_cnt; i++) {
		sources[i] = fopen(argv[argc - i - 1], "r");
                if (sources[i] == NULL) {
                	errx(EX_USAGE, "Error: can't open data file '%s'", argv[argc - i - 1]);
                }
	}

	// processing loop

	// dynamically allocate ips and sort_ips cause static allocation means lots of overhead if input small
        char *ips[MAX_SOURCES];
        char *sort_ips[MAX_SOURCES];
	int ends[MAX_SOURCES];
	int reads[MAX_SOURCES];
	unsigned int flen = 16;

	for (i=0; i<sources_cnt; i++) {
		ends[i] = 0;
		reads[i] = 1;
		ips[i] = NULL;
                sort_ips[i] = NULL;
	}

	// alloc memory, assume minimum size is 16 bytes (unencrypted IPv4s)
        for (i=0; i<sources_cnt; i++) {
                ips[i] = (char *) malloc(flen);
                sort_ips[i] = (char *) malloc(flen);
        }

	while (keep_going(ends)) {
		for (i=0; i<sources_cnt; i++) {
			if (reads[i]) {
				char s1[MAX_ITEM_LEN+1];
				if (fscanf(sources[i], "%"xstr(MAX_ITEM_LEN)"[^\n]\n", (char*)&s1) != EOF) {
					char *p = s1;
					char *field = NULL;

					j = 0;
					while (j <= idx) {
                        			field = strsep(&p, " ");
						// XXX no error checking here
                        			j++;
					}
                			// replace end of line 
                			p = strstr(field, "\n");
                			if (p != NULL) {
                        			*p = '\0';
                			}
					// realloc memory for all entries if necessary
                                        if (strlen(field)+1 > flen) {
                                                flen = strlen(field)+1;
                                                for (j=0; j<sources_cnt; j++) {
							ips[j] = (char *) realloc(ips[j], flen);
                                                        sort_ips[j] = (char *) realloc(sort_ips[j], flen);
                                                }
                                        }
					strcpy(ips[i], field);
				} else {
					ends[i] = 1;		
				}
			}
		}	

		/*for (i=0; i<sources_cnt; i++) {
			printf("%s ", ips[i]);
		}
		printf("\n");
		for (i=0; i<sources_cnt; i++) {
                        printf("%i ", ends[i]);
                }
                printf("\n");*/

		// find smallest IP of source we are not at the end already
		for (i=0; i<sources_cnt; i++) {
                        strcpy(sort_ips[i], ips[i]);
                }
		qsort(sort_ips, sources_cnt, sizeof(ips[0]), cmpstringp);

		/*for (i=0; i<sources_cnt; i++) {
                        printf("%s ", sort_ips[i]);
                }
                printf("\n");*/

		char *smallest = NULL;
		for (i=0; i<sources_cnt; i++) {
			int end = 0;
			// check if source ended already (suboptimal)
			for (j=0; j<sources_cnt; j++) {
				if (strcmp(sort_ips[i], ips[j]) == 0) {
					end = ends[j];
					break;
				}
			}

			if (!end) {
				smallest = sort_ips[i];
				break;
			}
		}

		if (smallest == NULL) {
			break;
		}

		//printf("smallest %s\n", smallest);

		int curr_entry = 0;
		for (i=0; i<sources_cnt; i++) {
			if (strcmp(smallest, ips[i]) == 0 && ! ends[i]) {
				curr_entry |= (1 << i);
				reads[i] = 1;
                       	} else {
				reads[i] = 0;
			}
		} 

		//printf("%i\n", curr_entry);

		// add one more occurance
        	counters[curr_entry] += 1;
	}

	if (sample_rate < 1.0) {
		for (i=0; i<rows; i++) {
			counters[i+1] = (unsigned long long) round((double)counters[i+1] / sample_rate);
		}
	}

	// output
	if (verbose) {
		printf("Final matrix:\n");
	}

	cnt = 1;
	for (i=0; i<rows-1; i++) {
		for (j=0; j<sources_cnt; j++) {	
			if (cnt & (1 << (sources_cnt - 1 - j))) {
				printf("1, ");
			} else {
				printf("0, ");
			}
		}
		printf("%lld\n", counters[cnt]);
		cnt++;
	}	

	if (out_fname != "") {
		FILE *outf = fopen(out_fname.c_str(), "w");
		cnt = 1;
        	for (i=0; i<rows; i++) {
                	for (j=0; j<sources_cnt; j++) {
                        	if (cnt & (1 << (sources_cnt - 1 - j))) {
                                	fprintf(outf, "1 ");
                        	} else {
                                	fprintf(outf, "0 ");
				}
                	}
                	fprintf(outf, "%lld\n", counters[cnt]);
                	cnt++;
        	}  
		fclose(outf);
	}

	// cleanup
	for (i=0; i<sources_cnt; i++) {
                free(ips[i]);
                free(sort_ips[i]);
        }

	for (i=0; i<sources_cnt; i++) {
		fclose(sources[i]);
	}
	free(counters);

	return 0;
}

