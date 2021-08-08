
import io

class ESENT_INDEX_ENTRY:
	def __init__(self):
		self.RecordPageKey = None

	@staticmethod
	def from_bytes(data):
		return ESENT_INDEX_ENTRY.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_INDEX_ENTRY()
		res.RecordPageKey = buff.read()
		return res