
from aesedb.structures.pageheader import readheader
from aesedb.structures.rootheader import ESENT_ROOT_HEADER
from aesedb.structures.branchheader import ESENT_BRANCH_HEADER
from aesedb.structures.spacetreeheader import ESENT_SPACE_TREE_HEADER
from aesedb.structures.spacetreeentry import ESENT_SPACE_TREE_ENTRY
from aesedb.structures.indexentry import ESENT_INDEX_ENTRY
from aesedb.structures.datadefinitionheader import ESENT_DATA_DEFINITION_HEADER
from aesedb.structures.leafentry import ESENT_LEAF_ENTRY
from aesedb.structures.branchentry import ESENT_BRANCH_ENTRY
from aesedb.structures.catalogdatadefentry import ESENT_CATALOG_DATA_DEFINITION_ENTRY

from aesedb.structures.leafheader import ESENT_LEAF_HEADER

from aesedb.utils.hexdump import hexdump
import enum
from struct import unpack


class WELLKNOWNPAGENO(enum.Enum):
	DATABASE           = 1
	CATALOG            = 4
	CATALOG_BACKUP     = 24

class PAGEFLAGS(enum.IntEnum):
	ROOT         = 1
	LEAF         = 2
	PARENT       = 4
	EMPTY        = 8
	SPACE_TREE   = 0x20
	INDEX        = 0x40
	LONG_VALUE   = 0x80
	NEW_FORMAT   = 0x2000
	NEW_CHECKSUM = 0x2000


class ESENT_PAGE:
	def __init__(self, db):
		self.db = db
		self.data = None
		self.record = None
		self.tags = {} # tagno -> (flags, data)
	
	async def read(self, data):
		try:
			self.data = data
			self.record, err = await readheader(self.db.Version, self.db.FileFormatRevision, self.db.PageSize, self.data)
			if err is not None:
				raise err
			return True, None
		except Exception as e:
			return None, e

	def printFlags(self):
		print(self.record.PageFlags)

	def dump(self):
		baseOffset = len(self.record)
		print(self.record)
		tags = self.data[-4*self.record.FirstAvailablePageTag:]

		print("FLAGS: ")
		self.printFlags()

		print()

		for i in range(self.record.FirstAvailablePageTag):
			tag = tags[-4:]
			if self.db.Version == 0x620 and self.db.FileFormatRevision > 11 and self.db.PageSize > 8192:
				valueSize = unpack('<H', tag[:2])[0] & 0x7fff
				valueOffset = unpack('<H',tag[2:])[0] & 0x7fff
				hexdump((self.data[baseOffset+valueOffset:][:6]))
				pageFlags = ord(self.data[baseOffset+valueOffset:][1]) >> 5
				#print "TAG FLAG: 0x%x " % (unpack('<L', self.data[baseOffset+valueOffset:][:4]) ) >> 5
				#print "TAG FLAG: 0x " , ord(self.data[baseOffset+valueOffset:][0])
			else:
				valueSize = unpack('<H', tag[:2])[0] & 0x1fff
				pageFlags = (unpack('<H', tag[2:])[0] & 0xe000) >> 13
				valueOffset = unpack('<H',tag[2:])[0] & 0x1fff
				
			print("TAG %-8d offset:0x%-6x flags:0x%-4x valueSize:0x%x" % (i,valueOffset,pageFlags,valueSize))
			#hexdump(self.getTag(i)[1])
			tags = tags[:-4]

		if self.record.PageFlags & PAGEFLAGS.ROOT > 0:
			rootHeader = ESENT_ROOT_HEADER(self.getTag(0)[1])
			print(rootHeader)
		elif self.record.PageFlags & PAGEFLAGS.LEAF == 0:
			# Branch Header
			flags, data = self.getTag(0)
			branchHeader = ESENT_BRANCH_HEADER(data)
			print(branchHeader)
		else:
			# Leaf Header
			flags, data = self.getTag(0)
			if self.record.PageFlags & PAGEFLAGS.SPACE_TREE > 0:
				# Space Tree
				spaceTreeHeader = ESENT_SPACE_TREE_HEADER(data)
				print(spaceTreeHeader)
			else:
				leafHeader = ESENT_LEAF_HEADER(data)
				print(leafHeader)

		# Print the leaf/branch tags
		for tagNum in range(1,self.record.FirstAvailablePageTag):
			flags, data = self.getTag(tagNum)
			if self.record.PageFlags & PAGEFLAGS.LEAF == 0:
				# Branch page
				branchEntry = ESENT_BRANCH_ENTRY(flags, data)
				print(branchEntry)
			elif self.record.PageFlags & PAGEFLAGS.LEAF > 0:
				# Leaf page
				if self.record.PageFlags & PAGEFLAGS.SPACE_TREE > 0:
					# Space Tree
					spaceTreeEntry = ESENT_SPACE_TREE_ENTRY(data)
					#print(spaceTreeEntry)

				elif self.record.PageFlags & PAGEFLAGS.INDEX > 0:
					# Index Entry
					indexEntry = ESENT_INDEX_ENTRY(data)
					#print(indexEntry)
				elif self.record.PageFlags & PAGEFLAGS.LONG_VALUE > 0:
					# Long Page Value
					raise Exception('Long value still not supported')
				else:
					# Table Value
					leafEntry = ESENT_LEAF_ENTRY(flags, data)
					dataDefinitionHeader = ESENT_DATA_DEFINITION_HEADER.from_bytes(leafEntry.EntryData)
					print(dataDefinitionHeader)
					catalogEntry = ESENT_CATALOG_DATA_DEFINITION_ENTRY.from_bytes(leafEntry.EntryData[len(dataDefinitionHeader):])
					print(catalogEntry)
					hexdump(leafEntry.EntryData)

	def get_tag(self, tagno):
		if self.record.FirstAvailablePageTag < tagno:
			raise Exception('Trying to grab an unknown tag 0x%x' % tagno)

		if tagno in self.tags:
			return self.tags[tagno]

		tags = self.data[-4*self.record.FirstAvailablePageTag:]
		baseOffset = self.record._len
		
		#input(tags)
		tag = tags[(-4*tagno)-4:-4*tagno]
		#input(calc_tag)

		#tag = tagno*4
		
		#### original
		#tags = self.data[-4*self.record.FirstAvailablePageTag:]
		#for i in range(tagno):
		#	tags = tags[:-4]
		#tag = tags[-4:]

		#input(tag)



		

		if self.db.Version == 0x620 and self.db.FileFormatRevision >= 17 and self.db.PageSize > 8192:
			valueSize = unpack('<H', tag[:2])[0] & 0x7fff
			valueOffset = unpack('<H',tag[2:])[0] & 0x7fff
			tmpData = list(self.data[baseOffset+valueOffset:][:valueSize])
			pageFlags = ord(tmpData[1]) >> 5
			tmpData[1] = chr(ord(tmpData[1:2]) & 0x1f)
			tagData = "".join(tmpData)
		else:
			valueSize = unpack('<H', tag[:2])[0] & 0x1fff
			pageFlags = (unpack('<H', tag[2:])[0] & 0xe000) >> 13
			valueOffset = unpack('<H',tag[2:])[0] & 0x1fff
			tagData = self.data[baseOffset+valueOffset:][:valueSize]
		
		self.tags[tagno] = (pageFlags, tagData)
		#return pageFlags, self.data[baseOffset+valueOffset:][:valueSize]
		return pageFlags, tagData