
import io
import enum

class CATALOG_TYPE(enum.Enum):
	TABLE        = 1
	COLUMN       = 2
	INDEX        = 3
	LONG_VALUE   = 4
	CALLBACK     = 5

class ESENT_CATALOG_DATA_DEFINITION_ENTRY:
	@staticmethod
	def from_bytes(data):
		return ESENT_CATALOG_DATA_DEFINITION_ENTRY.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		pos = buff.tell()
		buff.seek(4)
		dtype = CATALOG_TYPE(int.from_bytes(buff.read(2), byteorder='little', signed=False))
		buff.seek(pos)
		if dtype == CATALOG_TYPE.COLUMN:
			return ESENT_CATALOG_DATA_DEFINITION_ENTRY_COL.from_buffer(buff)
		elif dtype == CATALOG_TYPE.INDEX:
			return ESENT_CATALOG_DATA_DEFINITION_ENTRY_INDEX.from_buffer(buff)
		elif dtype == CATALOG_TYPE.TABLE:
			return ESENT_CATALOG_DATA_DEFINITION_ENTRY_TABLE.from_buffer(buff)
		elif dtype == CATALOG_TYPE.LONG_VALUE:
			return ESENT_CATALOG_DATA_DEFINITION_ENTRY_LV.from_buffer(buff)
		else:
			raise Exception('Unsupported type %s' % dtype)

class ESENT_CATALOG_DATA_DEFINITION_ENTRY_COL:
	def __init__(self):
		self.FatherDataPageID = None
		self.Type = None
		self.Identifier = None
		self.ColumnType= None
		self.SpaceUsage= None
		self.ColumnFlags= None
		self.CodePage= None
		self.Trailing = None
	
	@staticmethod
	def from_bytes(data):
		return ESENT_CATALOG_DATA_DEFINITION_ENTRY_COL.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_CATALOG_DATA_DEFINITION_ENTRY_COL()
		res.FatherDataPageID = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Type = CATALOG_TYPE(int.from_bytes(buff.read(2), byteorder='little', signed=False))
		res.Identifier = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.ColumnType= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.SpaceUsage= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.ColumnFlags= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.CodePage= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Trailing = buff.read()
		return res

class ESENT_CATALOG_DATA_DEFINITION_ENTRY_OTHER:
	def __init__(self):
		self.FatherDataPageID = None
		self.Type = None
		self.Identifier = None
		self.FatherDataPageNumber = None
		self.Trailing = None

	
	@staticmethod
	def from_bytes(data):
		return ESENT_CATALOG_DATA_DEFINITION_ENTRY_OTHER.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_CATALOG_DATA_DEFINITION_ENTRY_OTHER()
		res.FatherDataPageID = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Type = CATALOG_TYPE(int.from_bytes(buff.read(2), byteorder='little', signed=False))
		res.Identifier = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.FatherDataPageNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Trailing = buff.read()
		return res

class ESENT_CATALOG_DATA_DEFINITION_ENTRY_TABLE:
	def __init__(self):
		self.FatherDataPageID = None
		self.Type = None
		self.Identifier = None
		self.FatherDataPageNumber = None
		self.SpaceUsage = None
		self.Trailing = None

	
	@staticmethod
	def from_bytes(data):
		return ESENT_CATALOG_DATA_DEFINITION_ENTRY_TABLE.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_CATALOG_DATA_DEFINITION_ENTRY_TABLE()
		res.FatherDataPageID = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Type = CATALOG_TYPE(int.from_bytes(buff.read(2), byteorder='little', signed=False))
		res.Identifier = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.FatherDataPageNumber = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.SpaceUsage= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Trailing = buff.read()
		return res

class ESENT_CATALOG_DATA_DEFINITION_ENTRY_INDEX:
	def __init__(self):
		self.FatherDataPageID = None
		self.Type = None
		self.Identifier = None
		self.FatherDataPageNumber = None
		self.SpaceUsage = None
		self.IndexFlags = None
		self.Locale = None
		self.Trailing = None

	
	@staticmethod
	def from_bytes(data):
		return ESENT_CATALOG_DATA_DEFINITION_ENTRY_INDEX.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_CATALOG_DATA_DEFINITION_ENTRY_INDEX()
		res.FatherDataPageID = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Type = CATALOG_TYPE(int.from_bytes(buff.read(2), byteorder='little', signed=False))
		res.Identifier = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.FatherDataPageNumber = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.SpaceUsage= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.IndexFlags= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Locale= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Trailing = buff.read()
		return res

class ESENT_CATALOG_DATA_DEFINITION_ENTRY_LV:
	def __init__(self):
		self.FatherDataPageID = None
		self.Type = None
		self.Identifier = None
		self.FatherDataPageNumber = None
		self.SpaceUsage = None
		self.Trailing = None

	@staticmethod
	def from_bytes(data):
		return ESENT_CATALOG_DATA_DEFINITION_ENTRY_LV.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_CATALOG_DATA_DEFINITION_ENTRY_LV()
		res.FatherDataPageID = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Type = CATALOG_TYPE(int.from_bytes(buff.read(2), byteorder='little', signed=False))
		res.Identifier = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.FatherDataPageNumber = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.SpaceUsage= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Trailing = buff.read()
		return res
	