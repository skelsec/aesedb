
import io

class ESENT_DATA_DEFINITION_HEADER:
	def __init__(self):
		self._len = 4
		self.LastFixedSize = None
		self.LastVariableDataType = None
		self.VariableSizeOffset = None

	@staticmethod
	def from_bytes(data):
		return ESENT_DATA_DEFINITION_HEADER.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_DATA_DEFINITION_HEADER()
		res.LastFixedSize = int.from_bytes(buff.read(1), byteorder='little', signed=False)
		res.LastVariableDataType = int.from_bytes(buff.read(1), byteorder='little', signed=False)
		res.VariableSizeOffset = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		return res