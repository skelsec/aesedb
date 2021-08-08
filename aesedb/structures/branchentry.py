import io
import enum

class ESENT_TAGS(enum.IntFlag):
	UNKNOWN = 0x1
	DEFUNCT = 0x2
	COMMON  = 0x4


class ESENT_BRANCH_ENTRY_COMMON:
	def __init__(self):
		self.CommonPageKeySize = None
		self.LocalPageKeySize = None
		self.LocalPageKey = None
		self.ChildPageNumber = None
	
	@staticmethod
	def from_bytes(data):
		return ESENT_BRANCH_ENTRY_COMMON.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_BRANCH_ENTRY_COMMON()
		res.CommonPageKeySize = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.LocalPageKeySize = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.LocalPageKey = buff.read(res.LocalPageKeySize)
		res.ChildPageNumber = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		return res

class ESENT_BRANCH_ENTRY:
	def __init__(self):
		self.LocalPageKeySize = None
		self.LocalPageKey = None
		self.ChildPageNumber = None
	
	@staticmethod
	def from_bytes(data):
		return ESENT_BRANCH_ENTRY.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_BRANCH_ENTRY()
		res.LocalPageKeySize = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.LocalPageKey = buff.read(res.LocalPageKeySize)
		res.ChildPageNumber = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		return res

async def readbranchentry(flags, data):
	try:
		if ESENT_TAGS.COMMON in ESENT_TAGS(flags):
			return ESENT_BRANCH_ENTRY_COMMON.from_bytes(data), None
		return ESENT_BRANCH_ENTRY.from_bytes(data), None
	except Exception as e:
		return None, e