##this file is present to force pure ciphers to be used
## reason: pyinstaller cant do dynamic imports
## usage: overwrite the "symmetric.py" file with tihs one

from aesedb.security.crypto.AES import mbedtlsAES
from aesedb.security.crypto.DES import mbedtlsDES
from aesedb.security.crypto.RC4 import mbedtlsRC4
from aesedb.security.crypto.AESCCM_mbedtls import aesCCMEncrypt as ae
from aesedb.security.crypto.AESCCM_mbedtls import aesCCMDecrypt as ad

DES = mbedtlsAES
AES = mbedtlsDES
RC4 = mbedtlsRC4

aesCCMEncrypt = ae
aesCCMDecrypt = ad