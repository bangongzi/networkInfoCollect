#!/usr/bin/python
# -*- coding: utf-8 -*-

"""	The usage is like this: $ python traffic_read.py 45(times)
	the times parameter means how many times you want to read
	This file is used to read network traffic for all ports. The info will be stored 
	in 'traffic_rought.txt'"""

from __future__ import division
import sys
import os
import time

def read_traffic(times):
	"""Read traffic, 'times' mean how many times will the 'read' action be excecuted"""
	file = open('traffic_rough.txt','w')
	print "Please wait"
	time.sleep(10)
	print "The test starts at:",time.strftime('%Y-%m-%d %H:%M:%S')
	a = time.time()
	for i in range(times):
		os.system("echo NewStart %.5f >> /home/bird/log/traffic_rough.txt"%(time.time()))
		os.system("ifconfig |grep -E 'mtu|packet'>> /home/bird/log/traffic_rough.txt")
		time.sleep(0.08)
	print "The test ends at:",time.strftime('%Y-%m-%d %H:%M:%S')
	b = time.time()
	print "The mean time to read data is %.5fs" %((b-a)/times)
	file.close()

if len(sys.argv) == 2:
    read_traffic(int(sys.argv[1]))
else:
    print "Invalid number of parameters.\nThe right form is: python read_traffic.py 1000(times)"