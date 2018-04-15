#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
import os
import time


fname = 'ifconfig.txt'
file = open(fname,'w')
period = 3
print "The test starts at:",time.strftime('%Y-%m-%d %H:%M:%S')
a = time.time()
os.system("echo NewStart %.5f >> /home/per/log/%s"%( time.time(), fname ))
os.system("ifconfig |grep -A 20 s2-eth1|grep -E 'mtu|packet' >> /home/per/log/%s"%fname )
time.sleep(period)
os.system("echo ***Cutline***  >> /home/per/log/%s"%fname )
os.system("ifconfig |grep -A 20 s2-eth1|grep -E 'mtu|packet' >> /home/per/log/%s"%fname )
print "The test ends at:",time.strftime('%Y-%m-%d %H:%M:%S')
b = time.time()
print "The time cost is %f" %(b-a)
file.close
