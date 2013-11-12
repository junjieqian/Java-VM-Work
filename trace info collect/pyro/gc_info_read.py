#!/usr/bin/python
# gc_info_read.py

import string
import sys

def gc_read(filename):
    ''' Read in the GC happen time and translate it into integer
    @param time_list, gc time occurence list
    '''
    fp = open(filename, 'r')
    time_list = []
    for line in fp:
        if line.find('GC') >= 0:
            word = line.split(': ')
            time_list.append(str(float(word[0]))
    fp.close()
    return time_list

def range_read(filename):
    ''' Read in the heap range
    @param nursery_down, the bottom address range of nursery generation
    @param heap_up, the top address of heap
    @param heap_down, the bottom address range of heap
    '''
    fp = open(filename, 'r')
    for line in fp:
        if line.find('PSYoungGen ') >= 0:
            word = line.split('[')
            nursery_down = word[1].split(', ')[0]
            heap_up = word[1].split(', ')[1]
        if line.find('PSPermGen ') >= 0:
            word = line.split('[')
            heap_down = word[1].split(', ')[0]
    fp.close()
    return (nursery_down, heap_up, heap_down)
