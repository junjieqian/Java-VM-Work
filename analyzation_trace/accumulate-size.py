# !/usr/bin/python
# accumulate-size.py
# Author, Junjie Qian < jqian.unl@gmail.com >, Apr. 13 2013

''' 
We want to accumulate the size of new data brought in from the beginning of the trace for the purpose of determining 
how much new data has been brought in the cache between the creation of an object and its subsequent read accesses. 
So, first we maintain the cumulative size CS(i) with each Access(i). CS(i) retains the old value for read accesses 
but is updated for each new write access.
Using moving window to solve this problem. Fixed LLC size, if the accumulated object size larger than the LLC size, replace the first one.
'''

from argparse import RawTextHelpFormatter
from time import ctime
#from collections import OrderedDict
import argparse
import string

##### print out the help information and get the filename for trace/result
def getfilename():
	parser = argparse.ArgumentParser(
		description = "Large trace file analyzation, using accumulate the size algorithm. \n\tJunjie Qian, Mar. 2013", formatter_class= RawTextHelpFormatter)
	parser.add_argument("-source",
		help = "source trace filename, which should already be simplified (no continuous repeated), and follow the <operation mode> <address> <size>")
	parser.add_argument("-destination",
		help = "destination filename, which store the inter arrvial sizes in sequences of objects accessed. If not provided, a default one would be provided")

	args = parser.parse_args()
	print "The source file name is: ", args.source, " the destination file name is: ", args.destination

	sourcename = args.source
	targetname = args.destination

	return sourcename, targetname

##### do the calculation
def calculation(filename):
	fp = open(filename, 'r')
	linenum = 0							# the line number of each access
	addrmap = {}						# the hashmap of the addresses to avoid duplicate ones
	addrlist = []						# the list of the addresses in the order of placement
	targetlist = []						# the list of the target objects
	interlist = []						# the list of all the inter sizes
	intersizelist = []					# the list of one object's inter size
	accumulatesize = 0					# the accumulated total size

	intersize = 0						# the inter size between two accesses

	for line in fp:
		index = 0						# the index of the object in the target list
		index2 = 0
		intersize = 0
		word = string.split(line, ' ')
		mode = int(word[0])
		address = word[1]
		size = int(word[2])

		##### calculate the inter size, if the object still in the scope get the size, else the intersize equal to 8388608
		if address in targetlist:
			if addrmap.has_key(address):
				index = addrlist.index(address)
				for i in range(index, len(addrlist)):
					intersize += addrmap[addrlist[i]]
			else:
				intersize = 8388608
			intex2 = targetlist.index(address)
			intersizelist[index2].append(intersize)
		else:
			if mode == 1:
				targetlist.append(address)
				intersizelist.append([0])

		##### update the objects currently in the cache and get the updated accumulatesize
		if not addrmap.has_key(address):
			if accumulatesize+size <= 8388608:
				addrmap[address] = size
				addrlist.append(address)
				accumulatesize += size
			else:
				accumulatesize -= addrmap[addrlist[0]]
				addrmap[address] = size
				del addrmap[addrlist[0]]
				del addrlist[0]
				addrlist.append(address)
				accumulatesize += size
		else:
			addrlist.remove(address)
			addrlist.append(address) 

		linenum += 1
	fp.close()
	return targetlist, intersizelist

def savefile(filename, list1, list2):
	fp = open(filename, 'w')
	fp.write("Object list: \n")
	for element in list1:
		print >> fp, element
	fp.write("Inter size list: \n")
	for item in list2:
		print >> fp, item
	fp.close()

if __name__ == '__main__':
	sourcename, resultname = getfilename()
	list1 = []
	list2 = []
	list1, list2 = calculation(sourcename)
	print 'calculation ends'
	savefile(resultname, list1, list2)




