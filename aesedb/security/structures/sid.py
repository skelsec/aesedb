import io

class SAMR_RPC_SID_IDENTIFIER_AUTHORITY:
	def __init__(self):
		self.Value = None
	
	@staticmethod
	def from_bytes(data):
		return SAMR_RPC_SID_IDENTIFIER_AUTHORITY.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = SAMR_RPC_SID_IDENTIFIER_AUTHORITY()
		res.Value = buff.read(6)
		return res

class SAMR_RPC_SID:
	def __init__(self):
		self.Revision = None
		self.SubAuthorityCount = None
		self.IdentifierAuthority  = None
		self.SubLen  = None
		self.SubAuthority = None
	
	@staticmethod
	def from_bytes(data):
		return SAMR_RPC_SID.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = SAMR_RPC_SID()
		res.Revision = buff.read(1)[0]
		res.SubAuthorityCount = buff.read(1)[0]
		res.IdentifierAuthority  = SAMR_RPC_SID_IDENTIFIER_AUTHORITY.from_buffer(buff)
		res.SubLen  = res.SubAuthorityCount*4
		res.SubAuthority = buff.read()
		return res

	def __str__(self):
	   ans = 'S-%d-%d' % (self.Revision, ord(self.IdentifierAuthority.Value[5:6]))
	   for i in range(self.SubAuthorityCount):
		   t = int.from_bytes(self.SubAuthority[i*4:i*4+4], byteorder='big', signed = False)
		   ans += '-%d' % t
	   return ans