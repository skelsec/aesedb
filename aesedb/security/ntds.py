
import asyncio
from collections import OrderedDict
import traceback
from unicrypto.symmetric import RC4, AES, DES, MODE_CBC, MODE_ECB, deriveKey
from unicrypto.hashlib import md5

from aesedb.security.constants import NAME_TO_INTERNAL, ACCOUNT_TYPES, KERBEROS_TYPE
from aesedb.security.structures.pek import PEKLIST_ENC, PEK_KEY, PEKLIST_PLAIN
from aesedb.security.structures.crypted import CRYPTED_HASH, CRYPTED_HASHW16, CRYPTED_HISTORY, CRYPTED_BLOB
from aesedb.security.structures.userprops import USER_PROPERTIES
from aesedb.security.structures.kerbsecret import KERB_STORED_CREDENTIAL_NEW, KERB_KEY_DATA_NEW
from aesedb.security.structures.sid import SAMR_RPC_SID
from aesedb.security.common.usersecret import UserSecrets
from aesedb import logger
import datetime

from struct import unpack

NTDS_SUPPORTED_SECRET_TYPES = {
	NAME_TO_INTERNAL['objectSid'] : 1,
	NAME_TO_INTERNAL['dBCSPwd'] : 1,
	NAME_TO_INTERNAL['name'] : 1,
	NAME_TO_INTERNAL['sAMAccountType'] : 1,
	NAME_TO_INTERNAL['unicodePwd'] : 1,
	NAME_TO_INTERNAL['sAMAccountName'] : 1,
	NAME_TO_INTERNAL['userPrincipalName'] : 1,
	NAME_TO_INTERNAL['ntPwdHistory'] : 1,
	NAME_TO_INTERNAL['lmPwdHistory'] : 1,
	NAME_TO_INTERNAL['pwdLastSet'] : 1,
	NAME_TO_INTERNAL['userAccountControl'] : 1,
	NAME_TO_INTERNAL['supplementalCredentials'] : 1,
}


class NTDS:
	def __init__(self, db, bootkey):
		self.db = db
		self.bootkey = bootkey

		self.__PEK = []
		self.__cryptoCommon = None #CryptoCommon()
		self.__kerberosKeys = OrderedDict()
		self.__clearTextPwds = OrderedDict()
	
	async def open_db_table(self):
		try:
			logger.debug('Opening datatable...')
			cursor, err = await self.db.open_table('datatable')
			if err is not None:
				raise err
			return cursor, None
		except Exception as e:
			return None, e

	async def get_pek(self):
		try:
			logger.debug('Fetching PEK...')
			db_cursor, err = await self.open_db_table()
			if err is not None:
				raise err
			
			pklistname = NAME_TO_INTERNAL['pekList']
			peklist_enc = None
			while True:
				record, err = await self.db.get_next_row(db_cursor, {pklistname:1})
				if err is not None:
					raise err
				
				if record is None:
					raise Exception('PEK not found!')
				
				if pklistname in record and record[pklistname] is None:
					continue
				
				if pklistname in record:
					peklist_enc = PEKLIST_ENC.from_bytes(record[pklistname])
					break
			
			if peklist_enc is None:
				raise Exception('PEK not found!')

			#### decrypting peklist_enc
			if peklist_enc.Header[:4] == b'\x02\x00\x00\x00':
				# Up to Windows 2012 R2 looks like header starts this way
				
				ctx = md5(self.bootkey)
				for _ in range(1000):
					ctx.update(peklist_enc.KeyMaterial)
				tmpKey = ctx.digest()
				rc4 = RC4(tmpKey)
				peklist = PEKLIST_PLAIN.from_bytes(rc4.encrypt(peklist_enc.EncryptedPek))
				PEKLen = PEK_KEY()._len
				for i in range(len( peklist.DecryptedPek ) // PEKLen ):
					cursor = i * PEKLen
					pek = PEK_KEY.from_bytes(peklist.DecryptedPek[cursor:cursor+PEKLen])
					#print("PEK # %d found and decrypted: %s" % (i, pek['Key'].hex()))
					self.__PEK.append(pek.Key)

			elif peklist_enc.Header[:4] == b'\x03\x00\x00\x00':
				# Windows 2016 TP4 header starts this way
				# Encrypted PEK Key seems to be different, but actually similar to decrypting LSA Secrets.
				# using AES:
				# Key: the bootKey
				# CipherText: PEKLIST_ENC['EncryptedPek']
				# IV: PEKLIST_ENC['KeyMaterial']
				ctx = AES(self.bootkey, MODE_CBC, IV=peklist_enc.KeyMaterial)
				dec_pek = ctx.decrypt(peklist_enc.EncryptedPek)
				peklist = PEKLIST_PLAIN.from_bytes(dec_pek)

				# PEK list entries take the form:
				#   index (4 byte LE int), PEK (16 byte key)
				# the entries are in ascending order, and the list is terminated
				# by an entry with a non-sequential index (08080808 observed)
				pos, cur_index = 0, 0
				while True:
					pek_entry = peklist.DecryptedPek[pos:pos+20]
					if len(pek_entry) < 20: break # if list truncated, should not happen
					index, pek = unpack('<L16s', pek_entry)
					if index != cur_index: break # break on non-sequential index
					self.__PEK.append(pek)
					#print("PEK # %d found and decrypted: %s" % ( index, pek.hex()))
					cur_index += 1
					pos += 20

			logger.debug('PEK found and decrypted!')
			return True, None
		
		except Exception as e:
			return None, e
	
	def __removeDESLayer(self, cryptedHash, rid):
		Key1,Key2 = deriveKey(int(rid))
		Crypt1 = DES(Key1, MODE_ECB)
		Crypt2 = DES(Key2, MODE_ECB)
		decryptedHash = Crypt1.decrypt(cryptedHash[:8]) + Crypt2.decrypt(cryptedHash[8:])
		return decryptedHash
	
	def __removeRC4Layer(self, cryptedHash):
		# PEK index can be found on header of each ciphered blob (pos 8-10)
		pek_ixd = cryptedHash.Header[4]
		ctx = md5(self.__PEK[pek_ixd])
		ctx.update(cryptedHash.KeyMaterial)
		tmpKey = ctx.digest()
		rc4 = RC4(tmpKey)
		plainText = rc4.encrypt(cryptedHash.EncryptedHash)
		return plainText

	@staticmethod
	def __fileTimeToDateTime(t):
		t -= 116444736000000000
		t //= 10000000
		if t < 0:
			return 'never'
		else:
			dt = datetime.datetime.fromtimestamp(t)
			return dt.strftime("%Y-%m-%d %H-%M")
	
	def __decrypt_hash(self, secret: UserSecrets, record, db_cursor, with_history = True):
		try:
			try:
				sid = SAMR_RPC_SID.from_bytes(record[NAME_TO_INTERNAL['objectSid']])
				rid = str(sid).split('-')[-1]
			except Exception as e:
				print('SID parsing failed!')
				print('Data inpuit: %s' % record[NAME_TO_INTERNAL['objectSid']].hex())
				raise e
			secret.object_sid = sid
			#secret.rid = rid

			if record[NAME_TO_INTERNAL['dBCSPwd']] is not None:
				encryptedLMHash = CRYPTED_HASH.from_bytes(record[NAME_TO_INTERNAL['dBCSPwd']])
				if encryptedLMHash.Header[:4] == b'\x13\x00\x00\x00':
					# Win2016 TP4 decryption is different
					encryptedLMHash = CRYPTED_HASHW16.from_bytes(record[NAME_TO_INTERNAL['dBCSPwd']])
					pekIndex = encryptedLMHash.Header[4]
					ctx = AES(self.__PEK[pekIndex], MODE_CBC, IV=encryptedLMHash.KeyMaterial)
					dec_hash_temp = ctx.decrypt(encryptedLMHash.EncryptedHash[:16])
				else:
					dec_hash_temp = self.__removeRC4Layer(encryptedLMHash)
				secret.lm_hash = self.__removeDESLayer(dec_hash_temp, rid)
			else:
				secret.lm_hash = bytes.fromhex('aad3b435b51404eeaad3b435b51404ee')

			if record[NAME_TO_INTERNAL['unicodePwd']] is not None:
				encryptedNTHash = CRYPTED_HASH.from_bytes(record[NAME_TO_INTERNAL['unicodePwd']])
				if encryptedNTHash.Header[:4] == b'\x13\x00\x00\x00':
					# Win2016 TP4 decryption is different
					encryptedNTHash = CRYPTED_HASHW16.from_bytes(record[NAME_TO_INTERNAL['unicodePwd']])
					pekIndex = encryptedNTHash.Header[4]
					ctx = AES(self.__PEK[pekIndex], MODE_CBC, IV=encryptedNTHash.KeyMaterial)
					dec_hash_temp = ctx.decrypt(encryptedNTHash.EncryptedHash[:16])
				else:
					dec_hash_temp = self.__removeRC4Layer(encryptedNTHash)
				secret.nt_hash = self.__removeDESLayer(dec_hash_temp, rid)
			else:
				secret.nt_hash = bytes.fromhex('31d6cfe0d16ae931b73c59d7e0c089c0')

			if record[NAME_TO_INTERNAL['userPrincipalName']] is not None:
				secret.domain = record[NAME_TO_INTERNAL['userPrincipalName']].split('@')[-1]
				secret.username = '%s' % record[NAME_TO_INTERNAL['sAMAccountName']]
			else:
				secret.username = '%s' % record[NAME_TO_INTERNAL['sAMAccountName']]


			if record[NAME_TO_INTERNAL['userAccountControl']] is not None:
				secret.user_account_control = record[NAME_TO_INTERNAL['userAccountControl']]

			if record[NAME_TO_INTERNAL['pwdLastSet']] is not None:
				secret.pwd_last_set = self.__fileTimeToDateTime(record[NAME_TO_INTERNAL['pwdLastSet']])

			if with_history is False:
				return None, None

			if record[NAME_TO_INTERNAL['lmPwdHistory']] is not None:
				encryptedLMHistory = CRYPTED_HISTORY.from_bytes(record[NAME_TO_INTERNAL['lmPwdHistory']])
				tmpLMHistory = self.__removeRC4Layer(encryptedLMHistory)
				for i in range(0, len(tmpLMHistory) // 16):
					LMHash = self.__removeDESLayer(tmpLMHistory[i * 16:(i + 1) * 16], rid)
					secret.lm_history.append(LMHash)

			if record[NAME_TO_INTERNAL['ntPwdHistory']] is not None:
				encryptedNTHistory = CRYPTED_HISTORY.from_bytes(record[NAME_TO_INTERNAL['ntPwdHistory']])

				if encryptedNTHistory.Header[:4] == b'\x13\x00\x00\x00':
					# Win2016 TP4 decryption is different
					encryptedNTHistory = CRYPTED_HASHW16.from_bytes(record[NAME_TO_INTERNAL['ntPwdHistory']])
					pekIndex = encryptedNTHistory.Header[4]
					ctx = AES(self.__PEK[pekIndex], MODE_CBC, IV=encryptedNTHistory.KeyMaterial)
					dec_hash_temp = ctx.decrypt(encryptedNTHistory.EncryptedHash)
				else:
					dec_hash_temp = self.__removeRC4Layer(encryptedNTHistory)

				for i in range(0, len(dec_hash_temp) // 16):
					NTHash = self.__removeDESLayer(dec_hash_temp[i * 16:(i + 1) * 16], rid)
					secret.nt_history.append(NTHash)

			return True, None
		except Exception as e:
			return None, e

	def __decryptSupplementalInfo(self, secret: UserSecrets, record):
		try:
			haveInfo = False
			if record[NAME_TO_INTERNAL['supplementalCredentials']] is not None:
				if len(record[NAME_TO_INTERNAL['supplementalCredentials']]) > 24:
					cipherText = CRYPTED_BLOB.from_bytes(record[NAME_TO_INTERNAL['supplementalCredentials']])
					if cipherText.Header[:4] == b'\x13\x00\x00\x00':
						# Win2016 TP4 decryption is different
						pekIndex = cipherText.Header[4]
						ctx = AES(self.__PEK[pekIndex], MODE_CBC, IV=cipherText.KeyMaterial)
						plainText = ctx.decrypt(cipherText.EncryptedHash[4:])
						haveInfo = True
					else:
						plainText = self.__removeRC4Layer(cipherText)
						haveInfo = True
			
			
			if haveInfo is False:
				return True, None
			

			### woohooo we have info!
			try:
				userProperties = USER_PROPERTIES.from_bytes(plainText)
			except Exception as e:
				raise e
				# On some old w2k3 there might be user properties that don't
				# match [MS-SAMR] structure, discarding them
				return True, None
			
			for userprop in userProperties.UserProperties:
				if userprop.PropertyName == 'Primary:Kerberos-Newer-Keys':
					propertyValueBuffer = bytes.fromhex(userprop.PropertyValue.decode())
					kerbStoredCredentialNew = KERB_STORED_CREDENTIAL_NEW.from_bytes(propertyValueBuffer)
					data = kerbStoredCredentialNew.Buffer
					for credential in range(kerbStoredCredentialNew.CredentialCount):
						keyDataNew = KERB_KEY_DATA_NEW.from_bytes(data)
						data = data[keyDataNew._len:]
						keyValue = propertyValueBuffer[keyDataNew.KeyOffset:][:keyDataNew.KeyLength]

						if  keyDataNew.KeyType in KERBEROS_TYPE:
							#secret.kerberos_keys.append()
							answer =  (KERBEROS_TYPE[keyDataNew.KeyType],keyValue)
						else:
							answer =  (hex(keyDataNew.KeyType), keyValue)
						
						secret.kerberos_keys.append(answer)

				elif userprop.PropertyName == 'Primary:CLEARTEXT':
					# [MS-SAMR] 3.1.1.8.11.5 Primary:CLEARTEXT Property
					# This credential type is the cleartext password. The value format is the UTF-16 encoded cleartext password.
					try:
						secret.cleartext_pwds.append(userprop.PropertyValue.decode('utf-16le'))
					except UnicodeDecodeError:
						# This could be because we're decoding a machine password. Printing it hex
						secret.cleartext_pwds.append(userprop.PropertyValue.decode('utf-8'))
			
			return True, None
		except Exception as e:
			return None, e

	async def dump_secrets(self, only_ntlm = False, with_history = True, ignore_errors = True):
		try:
			_, err = await self.get_pek()
			if err is not None:
				raise err

			db_cursor, err = await self.db.open_table('datatable')
			if err is not None:
				raise err
			
			while True:
				await asyncio.sleep(0)
				record, err = await self.db.get_next_row(db_cursor, NTDS_SUPPORTED_SECRET_TYPES)
				if err is not None:
					raise err
				
				if record is None:
					#we parsed all
					return

				if len(record) != 0 and record[NAME_TO_INTERNAL['sAMAccountType']] in ACCOUNT_TYPES and NAME_TO_INTERNAL['objectSid'] in record:
					secret = UserSecrets()
					_, err = self.__decrypt_hash(secret, record, db_cursor, with_history)
					if err is not None:
						if ignore_errors is False:
							raise err
						continue
					
					if NAME_TO_INTERNAL['supplementalCredentials'] in record:
						_, err = self.__decryptSupplementalInfo(secret, record)
						if err is not None:
							if ignore_errors is False:
								raise err
							
					yield secret, None
					continue
				else:
					#for progress bar
					yield None, None

		except Exception as e:
			yield None, e
