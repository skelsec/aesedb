import io


class ESENT_PAGE_HEADER_2003_SP0:
	def __init__(self):
		self._len = 40
		self.CheckSum = None
		self.PageNumber = None
		self.LastModificationTime= None
		self.PreviousPageNumber= None
		self.NextPageNumber= None
		self.FatherDataPage= None
		self.AvailableDataSize= None
		self.AvailableUncommittedDataSize= None
		self.FirstAvailableDataOffset= None
		self.FirstAvailablePageTag= None
		self.PageFlags= None
	
	@staticmethod
	def from_bytes(data):
		return ESENT_PAGE_HEADER_2003_SP0.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_PAGE_HEADER_2003_SP0()
		res.CheckSum = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.PageNumber = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.LastModificationTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.PreviousPageNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.NextPageNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.FatherDataPage= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.AvailableDataSize= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.AvailableUncommittedDataSize= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.FirstAvailableDataOffset= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.FirstAvailablePageTag= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.PageFlags= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		return res

class ESENT_PAGE_HEADER_620_0b:
	def __init__(self):
		self._len = 44
		self.CheckSum = None
		self.ECCCheckSum = None
		self.LastModificationTime= None
		self.PreviousPageNumber= None
		self.NextPageNumber= None
		self.FatherDataPage= None
		self.AvailableDataSize= None
		self.AvailableUncommittedDataSize= None
		self.FirstAvailableDataOffset= None
		self.FirstAvailablePageTag= None
		self.PageFlags= None
	
	@staticmethod
	def from_bytes(data):
		return ESENT_PAGE_HEADER_620_0b.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_PAGE_HEADER_620_0b()
		res.CheckSum = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.ECCCheckSum = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.LastModificationTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.PreviousPageNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.NextPageNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.FatherDataPage= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.AvailableDataSize= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.AvailableUncommittedDataSize= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.FirstAvailableDataOffset= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.FirstAvailablePageTag= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.PageFlags= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		return res

class ESENT_PAGE_HEADER_WIN7:
	def __init__(self):
		self._len = 40
		self.CheckSum = None
		self.LastModificationTime= None
		self.PreviousPageNumber= None
		self.NextPageNumber= None
		self.FatherDataPage= None
		self.AvailableDataSize= None
		self.AvailableUncommittedDataSize= None
		self.FirstAvailableDataOffset= None
		self.FirstAvailablePageTag= None
		self.PageFlags= None
	
	@staticmethod
	def from_bytes(data):
		return ESENT_PAGE_HEADER_WIN7.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_PAGE_HEADER_WIN7()
		res.CheckSum = int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.LastModificationTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.PreviousPageNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.NextPageNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.FatherDataPage= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.AvailableDataSize= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.AvailableUncommittedDataSize= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.FirstAvailableDataOffset= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.FirstAvailablePageTag= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.PageFlags= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		return res

class ESENT_PAGE_HEADER_WIN7_EXT:
	def __init__(self):
		self._len = 80
		self.CheckSum = None
		self.LastModificationTime= None
		self.PreviousPageNumber= None
		self.NextPageNumber= None
		self.FatherDataPage= None
		self.AvailableDataSize= None
		self.AvailableUncommittedDataSize= None
		self.FirstAvailableDataOffset= None
		self.FirstAvailablePageTag= None
		self.PageFlags= None
		self.ExtendedCheckSum1 = None
		self.ExtendedCheckSum2 = None
		self.ExtendedCheckSum3 = None
		self.PageNumber = None
		self.Unknown = None
	
	@staticmethod
	def from_bytes(data):
		return ESENT_PAGE_HEADER_WIN7_EXT.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_PAGE_HEADER_WIN7_EXT()
		res.CheckSum = int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.LastModificationTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.PreviousPageNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.NextPageNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.FatherDataPage= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.AvailableDataSize= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.AvailableUncommittedDataSize= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.FirstAvailableDataOffset= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.FirstAvailablePageTag= int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.PageFlags= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.ExtendedCheckSum1= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.ExtendedCheckSum2= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.ExtendedCheckSum3= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.PageNumber= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.Unknown= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		return res


async def readheader(version, revision, pagesize=8192, data=None):
	try:
		if (version < 0x620) or (version == 0x620 and revision < 0x0b):
			return ESENT_PAGE_HEADER_2003_SP0.from_bytes(data), None
		elif version == 0x620 and revision < 0x11:
			# Exchange 2003 SP1 and Windows Vista and later
			return ESENT_PAGE_HEADER_620_0b.from_bytes(data), None
		else:
			if pagesize > 8192:
				return ESENT_PAGE_HEADER_WIN7_EXT.from_bytes(data), None
			return ESENT_PAGE_HEADER_WIN7.from_bytes(data), None
	except Exception as e:
		return None, e