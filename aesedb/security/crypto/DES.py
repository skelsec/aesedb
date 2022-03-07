"""
The idea here is to offer compatibility with 3rd party libraries by extending wrappers for ech encryption mode
This is needed because the pure python implementation for encryption and hashing algorithms are quite slow

currently it's not the perfect wrapper, needs to be extended
"""

from aesedb.security.crypto.BASE import symmetricBASE, cipherMODE
import aesedb.security.crypto.pure.DES.DES as _pyDES

try:
	from Crypto.Cipher import DES as _pyCryptoDES
except:
	pass

try:
	from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
	from cryptography.hazmat.backends import default_backend
except:
	pass

try:
	from Cryptodome.Cipher import DES as _pyCryptodomeDES
except:
	pass

try:
	from mbedtls import cipher as mbedcipher
except:
	pass

# from impacket
def expand_DES_key(key):
	# Expand the key from a 7-byte password key into a 8-byte DES key
	key  = key[:7]
	key += b'\x00'*(7-len(key))
	s  = (((key[0] >> 1) & 0x7f) << 1).to_bytes(1, byteorder = 'big')
	s += (((key[0] & 0x01) << 6 | ((key[1] >> 2) & 0x3f)) << 1).to_bytes(1, byteorder = 'big')
	s += (((key[1] & 0x03) << 5 | ((key[2] >> 3) & 0x1f)) << 1).to_bytes(1, byteorder = 'big')
	s += (((key[2] & 0x07) << 4 | ((key[3] >> 4) & 0x0f)) << 1).to_bytes(1, byteorder = 'big')
	s += (((key[3] & 0x0f) << 3 | ((key[4] >> 5) & 0x07)) << 1).to_bytes(1, byteorder = 'big')
	s += (((key[4] & 0x1f) << 2 | ((key[5] >> 6) & 0x03)) << 1).to_bytes(1, byteorder = 'big')
	s += (((key[5] & 0x3f) << 1 | ((key[6] >> 7) & 0x01)) << 1).to_bytes(1, byteorder = 'big')
	s += ( (key[6] & 0x7f) << 1).to_bytes(1, byteorder = 'big')
	return s
#

def deriveKey(baseKey):
	# 2.2.11.1.3 Deriving Key1 and Key2 from a Little-Endian, Unsigned Integer Key
	# Let I be the little-endian, unsigned integer.
	# Let I[X] be the Xth byte of I, where I is interpreted as a zero-base-index array of bytes.
	# Note that because I is in little-endian byte order, I[0] is the least significant byte.
	# Key1 is a concatenation of the following values: I[0], I[1], I[2], I[3], I[0], I[1], I[2].
	# Key2 is a concatenation of the following values: I[3], I[0], I[1], I[2], I[3], I[0], I[1]
	key = baseKey.to_bytes(4, byteorder='little', signed=False) #pack('<L',baseKey)
	key1 = [key[0] , key[1] , key[2] , key[3] , key[0] , key[1] , key[2]]
	key2 = [key[3] , key[0] , key[1] , key[2] , key[3] , key[0] , key[1]]
	return expand_DES_key(bytes(key1)),expand_DES_key(bytes(key2))

class pureDES(symmetricBASE):
	def __init__(self, key, mode = cipherMODE.ECB, IV = None):
		self.key = key
		if len(key) == 7:
			self.key = expand_DES_key(key)

		self.mode = mode
		self.IV = IV
		symmetricBASE.__init__(self)

	def setup_cipher(self):
		if self.mode == cipherMODE.ECB:
			mode = _pyDES.ECB
		elif self.mode == cipherMODE.CBC:
			mode = _pyDES.CBC
		else:
			raise Exception('Unknown cipher mode!')
		
		self._cipher = _pyDES.des(self.key, mode, self.IV)

	def encrypt(self, data):
		return self._cipher.encrypt(data)
	def decrypt(self, data):
		return self._cipher.decrypt(data)

class pyCryptodomeDES(symmetricBASE):
	def __init__(self, key, mode = cipherMODE.ECB, IV = None):
		self.key = key
		if len(key) == 7:
			self.key = expand_DES_key(key)

		self.mode = mode
		self.IV = IV
		symmetricBASE.__init__(self)

	def setup_cipher(self):
		if self.mode == cipherMODE.ECB:
			self._cipher = _pyCryptodomeDES.new(self.key, _pyCryptodomeDES.MODE_ECB)
		elif self.mode == cipherMODE.CBC:
			self._cipher = _pyCryptodomeDES.new(self.key, _pyCryptodomeDES.MODE_CBC, self.IV)
		else:
			raise Exception('Unknown cipher mode!')
		
	def encrypt(self, data):
		return self._cipher.encrypt(data)
	def decrypt(self, data):
		return self._cipher.decrypt(data)


class pyCryptoDES(symmetricBASE):
	def __init__(self, key, mode = cipherMODE.ECB, IV = None):
		self.key = key
		if len(key) == 7:
			self.key = expand_DES_key(key)

		self.mode = mode
		self.IV = IV
		symmetricBASE.__init__(self)

	def setup_cipher(self):
		if self.mode == cipherMODE.ECB:
			self._cipher = _pyCryptoDES.new(self.key)
		elif self.mode == cipherMODE.CBC:
			self._cipher = _pyCryptoDES.new(self.key, _pyCryptoDES.MODE_CBC, self.IV)
		else:
			raise Exception('Unknown cipher mode!')

	def encrypt(self, data):
		return self._cipher.encrypt(data)
	def decrypt(self, data):
		return self._cipher.decrypt(data)


class mbedtlsDES(symmetricBASE):
	def __init__(self, key, mode = cipherMODE.ECB, IV = None):
		self.key = key
		if len(key) == 7:
			self.key = expand_DES_key(key)

		self.mode = mode
		self.IV = IV
		symmetricBASE.__init__(self)

	def setup_cipher(self):
		if self.mode == cipherMODE.ECB:
			self._cipher = mbedcipher.DES.new(self.key, mbedcipher.MODE_ECB, b'')
		elif self.mode == cipherMODE.CBC:
			self._cipher = mbedcipher.DES.new(self.key, mbedcipher.MODE_CBC, self.IV)
		else:
			raise Exception('Unknown cipher mode!')

	def encrypt(self, data):
		return self._cipher.encrypt(data)
	def decrypt(self, data):
		return self._cipher.decrypt(data)