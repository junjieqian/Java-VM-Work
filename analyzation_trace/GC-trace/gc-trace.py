# !/bin/env/python
# gc-trace.py

import string
import os
import sys
from sys import argv
import matplotlib.pyplot as plt
import numpy as np

def getnames():
	try:
		script, tracename, resultname = argv
	except:
		sys.exit("Usage: python gc-trace.py trace-file-name result-file-name")

	return (tracename, resultname)

def readin(tracename):
	fp 				= open(tracename, 'r')
	addrlist 		= []	# used to store the addr list, indexed by different GC
	intersizelist 	= []	# used to store the inter size of different addr
	tempsizelist 	= []	# used to temp store inter size during each GC
	sizedict 		= {}   	# used to store last occur max size
	indexdict 		= {}  	# used to store the index in list
	templist 		= []	# used to store addr list during each GC
	maxaddr 		= 0
	idx 			= 0

	for line in fp:
		rw=1
		if line.find("GC")>0:  # this is one GC info, reset all elements
			maxaddr			= 0
			addrlist.append(templist)
			intersizelist.append(tempsizelist)
			tempsizelist	= []
			templist 		= []
			sizedict		= {}
			indexdict		= {}
			idx=0

		else:
			try:
				word=string.split(line, ' ')
				if word[2]=='R\n':
					rw=-1
			#	addr=int(word[0])*rw
				templist.append(addr)
				if (abs(addr)>maxaddr) and (abs(addr)>=0xa4c00000) and (abs(addr)<=0xafffffff):  # update the max addr in heap
					maxaddr 		= abs(addr)
				# if it happens once, record the passed memory size
				# update the sizedict
				if addr in sizedict:
					lastmaxaddr 	= sizedict[addr]
					sizedict[addr] 	= maxaddr
					index 			= indexdict[addr]
					tempsizelist[index].append(maxaddr-lastmaxaddr)
				else:
					print addr
					sizedict[addr] 	= maxaddr
					idx 			+= 1;
					templist.append(addr)
					tempsizelist.append([0])
					indexdict[addr] = idx

			except:
				pass

	print "Trace file finished"
	return (addrlist, intersizelist)

def plot(addrlist, resultname):
	i = 211

	plt.figure(1)
	plt.subplot(211)
	element = addrlist[0]
	t = np.arange(0, len(element), 1)
	plt.plot(t, element, '.')
	plt.subplot(212)
	element = addrlist[1]
	t = np.arange(0, len(element), 1)
	plt.plot(t, element, '.')
	plt.subplot(213)
	element = addrlist[2]
	t = np.arange(0, len(element), 1)
	plt.plot(t, element, '.')
	plt.savefig(resultname)

def main():
	(tracename,resultname) 	  = getnames();
	addrlist 				  = []
	intersizelist 			  = []
	(addrlist, intersizelist) = readin(tracename);
	for i in addrlist:
		print i
	plot(addrlist, resultname)

if __name__ == '__main__':
	main()
