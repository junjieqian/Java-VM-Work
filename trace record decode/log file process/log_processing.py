#!/usr/bin/env python
# log_processing.py

import sys
import string
import os
import logs

def helper():
	print "###################################################################################"
	print "# USAGE: ./log_processing.py log-file-path/file process-option"
	print "#   JVM Log file process options, "
	print "#      1. for logs with gc-verbose get the GC efficiency"
	print "#      2. for logs with PMU info, needs to be in pretty order to fetech the events"
	print "###################################################################################"

def main():
	try:
		script, filename, option = sys.argv
	except:
		sys.exit()

	if os.path.isfile(filename):
		logs.log_file_process(filename)
	else:
		logs.log_path_process(filename)