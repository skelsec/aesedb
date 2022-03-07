from mbedtls import cipher as mbedcipher

def aesGCMEncrypt(plaintext, aad, key, nonce, macLen = 16):
	cipher = mbedcipher.AES.new(key, mbedcipher.MODE_GCM,  nonce, aad)
	return cipher.encrypt(plaintext)

def aesGCMDecrypt(ciphertext, aad, key, nonce, macValue):
	cipher = mbedcipher.AES.new(key, mbedcipher.MODE_GCM,  nonce, aad)
	return cipher.decrypt(ciphertext)
