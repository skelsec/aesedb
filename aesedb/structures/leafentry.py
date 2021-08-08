import io

class ESENT_LEAF_ENTRY_COMMON:
	def __init__(self):
		self.CommonPageKeySize = None
		self.LocalPageKeySize = None
		self.LocalPageKey = None #  ('LocalPageKey',':'),
		self.EntryData = None # ('EntryData',':'),
	
	@staticmethod
	def from_bytes(data):
		return ESENT_LEAF_ENTRY_COMMON.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_LEAF_ENTRY_COMMON()
		res.CommonPageKeySize = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.LocalPageKeySize = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.LocalPageKey = buff.read(res.LocalPageKeySize)
		res.EntryData = buff.read()
		return res

class ESENT_LEAF_ENTRY:
	def __init__(self):
		self.LocalPageKeySize = None
		self.LocalPageKey = None #  ('LocalPageKey',':'),
		self.EntryData = None # ('EntryData',':'),
	
	@staticmethod
	def from_bytes(data):
		return ESENT_LEAF_ENTRY.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_LEAF_ENTRY()
		res.LocalPageKeySize = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.LocalPageKey = buff.read(res.LocalPageKeySize)
		res.EntryData = buff.read()
		return res

async def readleafentry(flags, data):
	try:
		if flags & 0x4 > 0:
			return ESENT_LEAF_ENTRY_COMMON.from_bytes(data), None
		return ESENT_LEAF_ENTRY.from_bytes(data), None

	except Exception as e:
		return None, e