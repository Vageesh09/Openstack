#!/usr/bin/env python

import time, sys
import clasTest as cs

class xx1():

	def __init__(self) :
		print "i a initialized1"

	def start1(self):
		m=cs.xx()
		m.start()
	
	

       

if __name__ == "__main__":
        daemon = xx1()
        daemon.start1()
               