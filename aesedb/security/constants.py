import enum

class SECRET_TYPE(enum.Enum):
	NTDS = 0
	NTDS_CLEARTEXT = 1
	NTDS_KERBEROS = 2

NAME_TO_INTERNAL = {
	'uSNCreated':b'ATTq131091',
	'uSNChanged':b'ATTq131192',
	'name':b'ATTm3',
	'objectGUID':b'ATTk589826',
	'objectSid':b'ATTr589970',
	'userAccountControl':b'ATTj589832',
	'primaryGroupID':b'ATTj589922',
	'accountExpires':b'ATTq589983',
	'logonCount':b'ATTj589993',
	'sAMAccountName':b'ATTm590045',
	'sAMAccountType':b'ATTj590126',
	'lastLogonTimestamp':b'ATTq589876',
	'userPrincipalName':b'ATTm590480',
	'unicodePwd':b'ATTk589914',
	'dBCSPwd':b'ATTk589879',
	'ntPwdHistory':b'ATTk589918',
	'lmPwdHistory':b'ATTk589984',
	'pekList':b'ATTk590689',
	'supplementalCredentials':b'ATTk589949',
	'pwdLastSet':b'ATTq589920',
}

NAME_TO_ATTRTYP = {
	'userPrincipalName': 0x90290,
	'sAMAccountName': 0x900DD,
	'unicodePwd': 0x9005A,
	'dBCSPwd': 0x90037,
	'ntPwdHistory': 0x9005E,
	'lmPwdHistory': 0x900A0,
	'supplementalCredentials': 0x9007D,
	'objectSid': 0x90092,
	'userAccountControl':0x90008,
}

ATTRTYP_TO_ATTID = {
	'userPrincipalName': '1.2.840.113556.1.4.656',
	'sAMAccountName': '1.2.840.113556.1.4.221',
	'unicodePwd': '1.2.840.113556.1.4.90',
	'dBCSPwd': '1.2.840.113556.1.4.55',
	'ntPwdHistory': '1.2.840.113556.1.4.94',
	'lmPwdHistory': '1.2.840.113556.1.4.160',
	'supplementalCredentials': '1.2.840.113556.1.4.125',
	'objectSid': '1.2.840.113556.1.4.146',
	'pwdLastSet': '1.2.840.113556.1.4.96',
	'userAccountControl':'1.2.840.113556.1.4.8',
}

KERBEROS_TYPE = {
	1:'dec-cbc-crc',
	3:'des-cbc-md5',
	17:'aes128-cts-hmac-sha1-96',
	18:'aes256-cts-hmac-sha1-96',
	0xffffff74:'rc4_hmac',
}

INTERNAL_TO_NAME = dict((v,k) for k,v in NAME_TO_INTERNAL.items())

SAM_NORMAL_USER_ACCOUNT = 0x30000000
SAM_MACHINE_ACCOUNT     = 0x30000001
SAM_TRUST_ACCOUNT       = 0x30000002

ACCOUNT_TYPES = ( SAM_NORMAL_USER_ACCOUNT, SAM_MACHINE_ACCOUNT, SAM_TRUST_ACCOUNT)