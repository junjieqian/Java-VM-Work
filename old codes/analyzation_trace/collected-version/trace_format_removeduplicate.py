# !/bin/env/python
# Junjie Qian, jqian@cse.unl.edu

# remove the duplicate access and keep only <operation mode> <object address> <size>, the input trace format is "1366129136863 0 0x61c11e94 123 4"

from sys import argv
import string

script, sourcename, resultname = argv

sourcefile = open(sourcename, 'r')
resultfile = open(resultname, 'w+')

i = 0
address = ""

for line in sourcefile:
	try:
		word = string.split(line, ' ')
		if not (word[2]==address):
			resultfile.write(word[1])
			resultfile.write(' ')
			resultfile.write(word[2])
                        resultfile.write(' ')
			resultfile.write(word[4])
		address = word[2]
		i += 1
	except:
		print i

sourcefile.close()
resultfile.close()


