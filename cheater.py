import sys,os,struct,subprocess,plistlib

sector_size=512
DEVICE = "/dev/"
class MBR(object):
	"""docstring for MBR"""
	def __init__(self,fpart):
		super(MBR, self).__init__()
		
		self.status,self.begHead,s2,s1,self._type = struct.unpack("<BBBBB",fpart[:5])
		#sector and cylinder are encoded in 2 bytes
		#15 14 13 12 11 10 9  8  7  6   6 4 3 2 1   0 
		#|--> CYL 7 to 0 <--  |<CYL8,9>|< - sector ->
		self.begSector = 0x3f & s2
		self.begCyl = ((0xc0 & s2)<<2)| s1
		self.endHead,s2,s1,self.LBA,self.numsec = struct.unpack("<BBBLL",fpart[5:16])
		self.endSector = 0x3f &s2
		self.endCyl = ((0xc0 & s2)<<2)| s1
class FAT(object):
	"""docstring for FAT"""
	def __init__(self, volID):
		super(FAT, self).__init__()
#		self.volID = volID
		self.bps,self.sect_per_cluster,self.num_res_sectors,self.num_of_fat = struct.unpack("<HBHB",volID[0x0B:0x0B+6])
		self.sect_per_fat = struct.unpack("<I",volID[0x24:0x24+4])[0]
		self.root_dir_fst_clust = struct.unpack("<I",volID[0x2C:0x2C+4])[0]
		self._sig = struct.unpack("<H",volID[0x1FE:0x1FE+2])[0]
		if self._sig != 43605:
			raise Exception("Bad Signature on FAT partition, should be 0x55/0xAA")
		if self.bps != 512 or self.num_of_fat !=2:
			raise Exception("Bad Fat partition header. not 512 bytes per sector or 2 fats not present")
		#compute begin of relevant information
	def calc_filesystem_offsets(self,hLBA):
		"""Calculate the offsets to read the actual filesystem"""
		self.fat_begin_lba = hLBA + self.num_res_sectors
		self.clust_begin_lba = self.fat_begin_lba + (self.num_of_fat*self.sect_per_fat)
		
		pass
	def clust_addrs(self,_clust_number):
		"""docstring for clust_addrs"""
		return self.clust_begin_lba +(_clust_number-2)*self.sect_per_cluster
def main():
	"""docstring for main"""
	
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
	
	self.disk=0
	DEVICE = "/dev/"+devList[rin]
	self.disk = file(DEVICE,'rb')
	disk.seek(0)
	print "Reading first sector (MBR)"
	first_sector = disk.read(1*sector_size)
	print "Getting Fat partition list"
	fat_part_list = (first_sector[-66:])[:64]
	print "Getting first partition descriptor"
	part1=fat_part_list[:16]
	# here on my drive I get this first partition, 
	#mind the endianness:
	#'80 |01 |01 |00 |06 |07 |E0 |D2 |20 |00 |00 |00 |E0 |D2 |03 |00 |'
	mbr = MBR(part1)
	self.disk.seek(sector_size*mbr.LBA)
	print "Getting LBA of first partition FAT descriptor"
	print "Reading firs sector of partition"
	volID = disk.read(1*sector_size)
	print "Analysing first sector"
	fat = FAT(volID)
	fat(calc_filesystem_offsets(mbr.LBA))
	self.disk.close()
	pass
	

def foutput(self,hxstr):
	"""docstring for foutput"""
	return ''.join( [ "%02X |" % ord( x ) for x in hxstr ] ).strip()
if __name__ == '__main__':
	main()