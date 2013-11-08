# !/bin/env/python
# address-divide-intersize.py

# divide the trace according to the address range

import string
import math
from sys import argv

script, sourcename, resultname, down = argv

sourcefile = open(sourcename, 'r')

#uplimit = 1.88*pow(10, 9)
#downlimit = 1.86*pow(10,9)
uplimit = (float(down)+0.01)*pow(10,9)
downlimit = float(down)*pow(10,9)
print "downlimit ", str(uplimit), " and uplimit ", str(downlimit)

targetmap = {}
targetlist = []
#intersizelist = []
sizelist = []

linenum = 0

addrlist = []
interlist = []
sizemap = {}

for line in sourcefile:
	begin = 0
	end = 0
	interlist = []
	intersize = 0
	word = string.split(line, ' ')
	rw = int(word[0])
	address = int(word[1], 16)
	size = int(word[2])
	addrlist.append(address)
	sizemap[address] = size

	if targetmap.has_key(address):
		begin = targetmap[address]
		end = linenum
		targetmap[address] = linenum

		for i in range(begin, end):
			interlist.append(addrlist[i])
		interlist = list(set(interlist))

		for i in range(0, len(interlist)):
			intersize += sizemap[interlist[i]]
		index = targetlist.index(address)
		sizelist[index].append(intersize)

	if (rw == 1) and (not targetmap.has_key(address)):
		if address>downlimit and address<uplimit:
			targetmap[address] = linenum
			targetlist.append(address)
			sizelist.append([0])

	linenum += 1

sourcefile.close()

resultfile = open(resultname, 'w+')
for item in targetlist:
	print >> resultfile, item
resultfile.write("inter sizes are:\n")
for element in sizelist:
	print >> resultfile, element
resultfile.close()


