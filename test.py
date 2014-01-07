#!/usr/bin/env python
# encoding: utf-8
"""
test.py.py

Created by Charles Romestant on 2011-09-13.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os,subprocess,plistlib


def main():
	ret=subprocess.check_output(["/usr/sbin/diskutil","list","-plist"])
	devTree= plistlib.readPlistFromString(ret)
	devList=[]
	counter =0
	frmt = """{0}- {1}
 With partitions :\n{2}"""
	print "Select device to format (Fat32 with MBR for now)"
	
	for dev in devTree["AllDisksAndPartitions"]:
		devList.append(dev['DeviceIdentifier'])
		print frmt.format(counter,devList[counter]+" of Size: "+str(dev["Size"])," \n".join(["    "+d["Content"]+" "+d["DeviceIdentifier"]+" Size:"+str(d["Size"]) for d in dev["Partitions"]]))
		counter +=1
	rin = int(raw_input("Choose your destiny -->"))
#ret = subprocess.check_output(["/usr/sbin/diskutil","unmountDisk","/dev/disk1"])

if __name__ == '__main__':
	main()

