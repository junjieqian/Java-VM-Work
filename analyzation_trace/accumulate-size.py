# !/usr/bin/python
# accumulate-size.py
# Author, Junjie Qian < jqian.unl@gmail.com >

''' 
We want to accumulate the size of new data brought in from the beginning of the trace for the purpose of determining 
how much new data has been brought in the cache between the creation of an object and its subsequent read accesses. 
So, first we maintain the cumulative size CS(i) with each Access(i). CS(i) retains the old value for read accesses 
but is updated for each new write access.
'''