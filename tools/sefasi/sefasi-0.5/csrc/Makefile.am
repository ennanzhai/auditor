
bin_PROGRAMS = sefasi_sample_items sefasi_encrypt_items sefasi_capture_data sefasi_set_intersect

AM_CXXFLAGS = -g -Wno-deprecated -Wall -O2

sefasi_sample_items_SOURCES = sefasi_sample_items.cc sefasi_common.h murmur3.h murmur3.c 
sefasi_encrypt_items_SOURCES = sefasi_encrypt_items.cc sefasi_common.h ini.h ini.c INIReader.h INIReader.cpp
sefasi_capture_data_SOURCES = sefasi_capture_data.cc sefasi_common.h
sefasi_set_intersect_SOURCES = sefasi_set_intersect.cc sefasi_common.h

sefasi_encrypt_items_LDADD = @CRYPTOLIB@ 

#dist_man8_MANS = sefasi_sample_items.8 sefasi_encrypt_items.8 sefasi_capture_data.8 sefasi_set_intersect.8
