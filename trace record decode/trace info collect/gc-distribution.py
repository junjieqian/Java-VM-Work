#!/usr/bin/python
# gc-distribution.py
# using this to verify the access patern of objects arount each gc

import second_gc_log
import millisecond_gc_log
import sys
import string

def main():
    try:
        script, filename, gclog, cachefile, fullcachein = sys.argv
    except:
        sys.exit("USAGE: python gc-prefetch-verify.py trace-file-name gc-log-file output-cache-file-name-without-BIAS output-cache-file-name")

    fp = open(filename, 'r')
    firstline = fp.readline()
    fp.close()
    if int(firstline.split('\n')[0], 0) > 414086872:
        second_gc_log.second_gc_log(filename, gclog, cachefile, fullcachein)
    else:
        millisecond_gc_log.millisecond_gc_log(filename, gclog, cachefile, fullcachein)

if __name__=='__main__':
    main()
