#!/usr/bin/env Python
# ET-log is log trace file got with Elephant Track

import string
import sys
from pkg import tracefile

def helper():
  print "Usage: python main.py file-name option"
  print "file-name, Elephant track log file name"
  print "options: 0, trace-file input format"

def main():
  try:
    script, filename, option = sys.argv
  except:
    helper()
    sys.exit("\n")
  if option == '0':
    print "shared objects number: ", tracefile.tracefile(filename)
  elif option == '1':
  	pass

if __name__ == "__main__":
  main()