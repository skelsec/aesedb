from mbedtls import cipher as mbedcipher

def aesCCMEncrypt(plaintext, aad, key, nonce, macLen = 16):
	cipher = mbedcipher.AES.new(key, mbedcipher.MODE_CCM,  nonce, aad)
	return cipher.encrypt(plaintext)

def aesCCMDecrypt(ciphertext, aad, key, nonce, macValue):
	cipher = mbedcipher.AES.new(key, mbedcipher.MODE_CCM, nonce, aad)
	return cipher.decrypt(ciphertext, macValue)
