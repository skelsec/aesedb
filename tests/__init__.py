
import unittest
import asyncio
import pathlib


class NTDSParse:
	async def runner(self, parser, out_q):
		_, err = await parser.run()
		if err is not None:
			await out_q.put((None, None, err, True))

	async def parser_test(self, crypolibname):
		try:
			import unicrypto
			unicrypto.use_library(crypolibname)
			from aesedb.examples.ntdsparse import NTDSParserConsole
			from .knownvalues import knowngood
			basepath = pathlib.Path(__file__).parent.resolve()
			ntdsfile = str(basepath.joinpath('ntds.dit'))
			systemfile = str(basepath.joinpath('SYSTEM'))

			lm_deleted = {}
			nt_deleted = {}

			out_q = asyncio.Queue()
			parser = NTDSParserConsole(systemfile, ntdsfile, show_progress = True, outfile = None, ext_result_q=out_q, count_total = False)
			x = asyncio.create_task(self.runner(parser, out_q))
			while True:
				usersecret, total, err, eof = await out_q.get()
				
				if err is not None:
					raise err
				if eof is True:
					break
				if usersecret is None:
					continue
				
				for secret in str(usersecret).split('\r\n'):
					ht, *t = secret.split(':')
					if ht == 'ntlm':
						domain, user, rid, sid, lm, nt, lastset_or_history = t
						if lm not in lm_deleted:
							del knowngood['lmhashes'][lm]
							lm_deleted[lm] = 1
						if nt not in nt_deleted:
							del knowngood['nthashes'][nt]
							nt_deleted[nt] = 1
					elif ht == 'kerberos':
						domain, user, sid, kt, secret = tuple(t)
					elif ht == 'cleartext':
						domain, user, sid, secret = tuple(t)
				
			if len(knowngood['lmhashes']) > 0:
				raise Exception('LM hashes remaining: %s' % len(knowngood['lmhashes']))
				
			if len(knowngood['nthashes']) > 0:
				raise Exception('NT hashes remaining: %s' % len(knowngood['nthashes']))
			with open('remaining_nt.txt', 'w', newline = '') as f:
				for x in knowngood['nthashes']:
					f.write(x + '\r\n')
			return True, None
		except Exception as e:
			print(e)
			return False, e


#class pure(NTDSParse, unittest.IsolatedAsyncioTestCase):	
#	async def test_parser(self):
#		_, err = await self.parser_test('pure')
#		if err is not None:
#			raise err
#
#class Crypto(NTDSParse, unittest.IsolatedAsyncioTestCase):
#	async def test_parser(self):
#		_, err = await self.parser_test('pure')
#		if err is not None:
#			raise err
#
#class pyCryptodome(NTDSParse, unittest.IsolatedAsyncioTestCase):
#	async def test_parser(self):
#		_, err = await self.parser_test('pure')
#		if err is not None:
#			raise err
#
#class MBEDTLS(NTDSParse, unittest.IsolatedAsyncioTestCase):
#	async def test_parser(self):
#		_, err = await self.parser_test('pure')
#		if err is not None:
#			raise err

class cryptography(NTDSParse, unittest.IsolatedAsyncioTestCase):
	async def test_parser(self):
		_, err = await self.parser_test('pure')
		if err is not None:
			raise err

if __name__ == '__main__':
	unittest.main()