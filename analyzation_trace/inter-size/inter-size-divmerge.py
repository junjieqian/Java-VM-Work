# !/bin/python
# Junjie Qian, jqian@cse.unl.edu
# 
# 
# calculation of the inter arrival size between the initialized objects (first write and then first use).
# this is for the extremly large trace file, using database to store and fetch information
# 1st version, 03/19/2013
# the input file is supposed to have the replicated ones erased, and each line format is "<operation mode> <address> <size>"

from argparse import RawTextHelpFormatter
from time import ctime
import argparse
import string, os


###################### split file into several small pieces
def splitfile(filename):
	file_handler = open(filename, 'r')
	block_size = 10000000
	countfile = 0
	linestring = []
	i = 0
	if not os.path.exists(filename+'_split'):
		os.makedirs(filename+'_split')
	for line in file_handler:
		if i == (block_size-1):
			file_writer = open(filename + '_split/file_' + str(countfile), 'a+')
			file_writer.writelines(linestring)
			file_writer.close()
			linestring = []
			countfile += 1
			i = 0
			print "\tfile" + str(countfile) + "generated at " + str(ctime())
		else:
			linestring.append(line)
			i += 1

	if len(linestring) >0:
		file_writer = open(filename + '_split/file_' + str(countfile), 'a+')
		file_writer.writelines(linestring)
		file_writer.close()
		linestring = []
		print "\tfile" + str(countfile) + "generated at " + str(ctime())
	file_handler.close()

##################### process the small pieces data files
##################### one assumption here is if the inter arrival lines is larger than 10^9, the inter arrival size is supposed as 8MB.
def calculation(sourcename, countfilenum, inter_size_list, object_list):
	sourcefile = open(sourcename + '_split/file_' + str(countfilenum), 'r')
#	sourcefile = open(sourcename, 'r')
	print sourcename + '_split/file_' + str(countfilenum)
#	tmpsourceusage = string.split(sourcename, 'file_')
#	tmpsourcefilename = tmpsourceusage[0]+'file_'+str(countfilenum-1)
	tmpsourcefilename = sourcename + '_split/file_' + str(countfilenum-1)
	print tmpsourcefilename
	object_map = {}
	size_map = {}
	###### the following two should be global variable
	#object_list = []
	#inter_size_list = []
	###################################################
	addr_list = []
	inter_list = []
	line = 0 + (countfilenum * 10000000)
	begin = 0
	end = 0
	object_index = 0
	inter_size = 0
	for linestr in sourcefile:
		word = string.split(linestr, ' ')
		rw = int(word[0])
		address = word[1]
		size = int(word[2])
		addr_list.append(address)
		inter_size = 0
		if not size_map.has_key(address):
			size_map[address] = size

		if (object_map.has_key(address)):
			begin = object_map[address]
			end = line
			object_map[address] = line

			if not(address in object_list):
				object_list.append(address)
				inter_size_list.append([0])

			if (end-begin)>5000000:
				inter_size = 8388608
			else:
				if (begin>=(countfilenum * 10000000)):  # means two in the same file
					begin = begin - (countfilenum * 10000000)
					end = end - (countfilenum * 10000000)
					for i in range(begin, end):
						inter_list.append(addr_list[i])
					inter_list = list(set(inter_list))
					tmp = 0
					for j in range(0, len(inter_list)):
						if (inter_size>=8388608):
							inter_size = 8388608
							break
						else:
							if (tmp+size_map[inter_list[j]])<64:
								tmp += size_map[inter_list[j]]
							else:
								tmp = (tmp+size_map[inter_list[j]]) - (64*int((tmp+size_map[inter_list[j]])/64))
								inter_size += 64*int((tmp+size_map[inter_list[j]])/64)
				else:
					end = end - (countfilenum * 10000000)
					for k in range (0, end):
						inter_list.append(addr_list[k])
					tmpfile = open(tmpsourcefilename, 'r')
					m = 0
					for lines in tmpfile:
						m += 1
						tmp_addr = string.split(lines, ' ')[1]
						size_map[tmp_addr] = string.split(lines, ' ')[2]
						begin = begin - ((countfilenum-1) * 10000000)
						if m > begin:
							inter_list.append(tmp_addr)
					inter_list = list(set(inter_list))
					tmp = 0
					for l in range(0, len(inter_list)):
						if (inter_size>=8388608):
							inter_size = 8388608
							break
						else:
							if (tmp+size_map[inter_list[l]])<64:
								tmp += size_map[inter_list[l]]
							else:
								tmp = (tmp+size_map[inter_list[l]]) - (64*int((tmp+size_map[inter_list[l]])/64))
								inter_size += 64*int((tmp+size_map[inter_list[l]])/64)

			# get the index of this target in the target list
			object_index = object_list.index(address)
			#print object_index
			inter_size_list[object_index].append(inter_size)
			del inter_list[:]

		if (rw==1) and (not object_map.has_key(address)):
			object_map[address] = line
		line += 1
	return inter_list, object_list

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description = "Large trace file analyzation, using divide them into small pieces and merge the result, \n\t Junjie Qian, Mar. 2013", formatter_class= RawTextHelpFormatter)
	parser.add_argument("-source",
		help = "source trace filename, which should already be simplified (no continuous repeated), and follow the <operation mode> <address> <size>")
	parser.add_argument("-destination",
		help = "destination filename, which store the inter arrvial sizes in sequences of objects accessed")

	args = parser.parse_args()
	print args.source, args.destination

#	splitfile(args.source)

	count = 0
	inter_size_list = []
	object_list = []
'''
	for root, dirs, files in os.walk(args.source+'_split'):
		for f in files:
			print args.source+'_split'
			sourcefile = os.path.join(args.source+'_split', f)
			#inter_list, object_list = calculation(sourcefile, count, inter_size_list, object_list)
			print sourcefile
			count += 1
'''

	path, dirs, files = os.walk(args.source+'_split').next()
	countfile = len(files)
	print countfile

	for count in range(0, countfile):
		sourcefile = args.source
		inter_list, object_list = calculation(sourcefile, count, inter_size_list, object_list)

#	print inter_list
	resultfile = open(args.destination, 'w+')
	resultfile.write('inter size list: \n')
	for item2 in inter_size_list:
		print >> resultfile, item2
	resultfile.close()

