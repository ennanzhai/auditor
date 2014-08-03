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

    sefasi_encrypt_items.cc
    Encrypt items 

    $Id: sefasi_encrypt_items.cc 644 2013-08-15 05:27:44Z szander $
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
#include <openssl/rsa.h>
#include <openssl/engine.h>
#include <openssl/err.h>
#include <openssl/bn.h>

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <string>

#include "sefasi_common.h"
#include "INIReader.h"


using namespace std;



// globals

// verbosity level
int verbose = 0;


// print usage
void usage(char *name)
{

	cout << "Usage: " << name << " [OPTIONS] <-|item_list> " << endl;
	cout << "       -c <public_config>                      public config file name" << endl;
	cout << "       -h                                      show usage" << endl;
	cout << "       -i <index>         			index of input file that contains IP addresses" << endl;
	cout << "       -I          				specify that the input items are IPv4 addresses" << endl;
	cout << "       -p <private_config>          		private config file name" << endl;
	cout << "       -v       				enable verbose mode" << endl;
	cout << "       <-|item_list>      			file name to read item from or '-' to read from stdin" << endl;

}


int main(int argc, char **argv)
{
	int c;
	char *endptr;
	opterr = 0;
	FILE *item_file;

	string cfg_fname = "";
	string pcfg_fname = ""; 
	int input_is_ipv4s = 0;
	unsigned int idx = 0;
	RSA *rsa_obj;
	BIGNUM *n = NULL, *p = NULL, *q = NULL, *e = NULL;

	//srand48(time(NULL));
	//srandom(time(NULL));

	while ((c = getopt(argc, argv, "c:hi:Ip:v")) != -1) {
		switch (c)
		{
			case 'c':
				cfg_fname = string(optarg);
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
				input_is_ipv4s = 1;
				break;

			case 'p':
				pcfg_fname = string(optarg);
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

	if (cfg_fname == "") {
		errx(EX_USAGE, "Error: No public config file");
	}
	if (pcfg_fname == "") {
                errx(EX_USAGE, "Error: No private config file");
        }

	// open config files and read config

	INIReader cfg_reader(cfg_fname);
	INIReader pcfg_reader(pcfg_fname);

    	if (cfg_reader.ParseError() < 0) {
		errx(EX_USAGE, "Error: Can't read public config file");
    	}
	if (pcfg_reader.ParseError() < 0) {
                errx(EX_USAGE, "Error: Can't read private config file");
        }

	if (cfg_reader.Get("encryption", "p", "") == "" ||
	    cfg_reader.Get("encryption", "q", "") == "") {
		errx(EX_USAGE, "Error: primes p and q must be defined in public config");
	}

	string pstr = cfg_reader.Get("encryption", "p", ""); 
	BN_dec2bn(&p, pstr.c_str());
	string qstr = cfg_reader.Get("encryption", "q", ""); 
	BN_dec2bn(&q, qstr.c_str());

	// get private key
	if (pcfg_reader.Get("encryption", "private_key", "") == "") {
		errx(EX_USAGE, "Error: private key must be defined in private config");
	}

	string estr = pcfg_reader.Get("encryption", "private_key", ""); 
	BN_dec2bn(&e, estr.c_str());

	if (BN_cmp(p, q) > 1) {
		BIGNUM *tmp;
		tmp = q;
		q = p;
		p = tmp;
	}

	BN_CTX *ctx = BN_CTX_new();
	if (ctx == NULL) {
		errx(EX_DATAERR, "Error: failed to allocate BN context");	
	}

	n = BN_new();
	BN_mul(n, p, q, ctx);

        //printf("%s\n", BN_bn2dec(p));
        //printf("%s\n", BN_bn2dec(q));
        //printf("%s\n", BN_bn2dec(n));
        //printf("%s\n", BN_bn2dec(e));

	ERR_load_crypto_strings();

	rsa_obj = RSA_new();
	rsa_obj->n = n;
	rsa_obj->p = p;
	rsa_obj->q = q;
	rsa_obj->e = e;
	rsa_obj->d = NULL;
	rsa_obj->dmp1 = NULL;
	rsa_obj->dmq1 = NULL;
	rsa_obj->iqmp = NULL;

	if (BN_num_bits(rsa_obj->n) > OPENSSL_RSA_MAX_MODULUS_BITS) {
		errx(EX_USAGE, "Error: modulus too large");
        }

        if (BN_ucmp(rsa_obj->n, rsa_obj->e) <= 0) {
		errx(EX_USAGE, "Error: bad encryption key value");
        }

        // for large moduli, enforce exponent limit
        if (BN_num_bits(rsa_obj->n) > OPENSSL_RSA_SMALL_MODULUS_BITS) {
                if (BN_num_bits(rsa_obj->e) > OPENSSL_RSA_MAX_PUBEXP_BITS) {
			errx(EX_USAGE, "Error: bad encryption key value");
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
	//unsigned char cipher[MAX_ITEM_LEN+1];
	unsigned long line = 0;

	//memset(s1, 0, RSA_size(rsa_obj));
	//memset(cipher, 0, RSA_size(rsa_obj));

	BIGNUM *in = BN_new();
	BIGNUM *ret = BN_new();
	BIGNUM *f = BN_new();

	while (fscanf(item_file, "%"xstr(MAX_ITEM_LEN)"[^\n]\n", (char*)&s1) != EOF) {
		unsigned int i = 0;
		char *field = NULL;
		char *p = s1;
		int ilen;

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

		if (input_is_ipv4s) {
			ilen = strlen(field);
		} else {
			// convert number string to bn and then to binary 
			BN_dec2bn(&in, field);
			BN_bn2bin(in, (unsigned char *)field);
			ilen = BN_num_bytes(in);
		}

		// use RSA encryption function 
		/*int len;
		if ((len = RSA_public_encrypt(RSA_size(rsa_obj), (unsigned char *)field, cipher, 
				rsa_obj, RSA_NO_PADDING)) < 0) {
			errx(EX_DATAERR, "Error: encryption error: %s", ERR_error_string(ERR_get_error(), NULL));
		}
		BN_bin2bn(cipher, len, ret);
		*/

		// compute exponentiation and modulus directly (avoiding overhead)
		BN_bin2bn((unsigned char *)field, ilen, f);
		if (BN_ucmp(f, rsa_obj->n) >= 0) {
                        errx(EX_DATAERR, "Error: input data too large for modulus");
                }
		BN_mod_exp(ret, f, rsa_obj->e, rsa_obj->n, ctx);

		/*printf("%s\n", field);
		for (i=0; i<(unsigned int)len; i++) {
                        printf("%d ", (int) field[i]);
                }
                printf("\n");
		for (i=0; i<(unsigned int)len; i++) {
			printf("%d ", (int) cipher[i]);
		}
		printf("\n");*/

		char *num_str = BN_bn2dec(ret);
		printf("%s\n", num_str);
		OPENSSL_free(num_str);

		//memset(s1, 0, RSA_size(rsa_obj));
		
		line++;
	}

	fclose(item_file);

	BN_free(in);
	BN_free(ret);

	ERR_free_strings();

	RSA_free(rsa_obj);

	BN_CTX_free(ctx);

	return 0;
}

