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
	   ####################################################################
	   # WARNING - DO NOT "FIX" THIS BYTE ORDER. READ THIS FIRST.
	   #
	   # This class is internal to the NTDS DIT (ESE) parser. All other
	   # code paths in aiosmb/octopwn use winacl's SID class, which is the
	   # canonical, MS-DTYP-correct implementation.
	   #
	   # Sub-authorities are deliberately decoded big-endian here because
	   # ntds.py extracts the RID for DES key derivation via:
	   #     rid = str(sid).split('-')[-1]
	   # and the on-disk NTDS objectSid encoding stores the trailing
	   # sub-authority (the RID) in big-endian. Decoding it big-endian here
	   # is what produces the integer that AD originally used as the DES
	   # key seed (unicrypto.symmetric.deriveKey), so changing this to
	   # 'little' will silently corrupt every LM/NT hash, hash history and
	   # supplemental-credential blob coming out of offline NTDS parsing.
	   # See impacket's NTDSHashes.__getOfflineDatatableSidComponents for
	   # the same observation in the reference implementation.
	   #
	   # As a side effect, the domain-prefix sub-authorities printed by
	   # this __str__ are byte-swapped relative to the canonical SID. If
	   # you need a human/storage-facing canonical SID string, call
	   # formatCanonical() instead - it mixes the byte orders correctly.
	   ####################################################################
	   ans = 'S-%d-%d' % (self.Revision, ord(self.IdentifierAuthority.Value[5:6]))
	   for i in range(self.SubAuthorityCount):
		   t = int.from_bytes(self.SubAuthority[i*4:i*4+4], byteorder='big', signed = False)
		   ans += '-%d' % t
	   return ans

	def formatCanonical(self):
		# Canonical, human/storage-facing SID string for an NTDS-parsed SID.
		#
		# The on-disk NTDS objectSid encoding is mixed-endian: the domain-
		# prefix sub-authorities are stored little-endian (matching the
		# MS-DTYP wire format), but the final sub-authority (the RID) is
		# stored big-endian. Mirror that here so the resulting string
		# matches what LDAP/winacl produces for the same security
		# principal. See impacket secretsdump's
		# NTDSHashes.__getOfflineDatatableSidComponents for the same
		# workaround in the reference implementation.
		#
		# IMPORTANT: __str__ deliberately stays big-endian for every
		# sub-authority because ntds.py's decryption path depends on it.
		# Do not route the decryption RID through formatCanonical().
		ans = 'S-%d-%d' % (self.Revision, ord(self.IdentifierAuthority.Value[5:6]))
		n = self.SubAuthorityCount
		for i in range(n):
			chunk = self.SubAuthority[i*4:i*4+4]
			order = 'big' if i == n - 1 else 'little'
			ans += '-%d' % int.from_bytes(chunk, byteorder=order, signed=False)
		return ans