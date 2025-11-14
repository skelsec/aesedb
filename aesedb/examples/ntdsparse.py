import asyncio
from tqdm import tqdm
from aesedb.eesentdb import ESENT_DB
from aesedb.utils.afile import AFile
from aesedb.security.ntds import NTDS
from aesedb.utils.systemhive import SYSTEM
from aiowinreg.ahive import AIOWinRegHive
from aesedb import logger
import json

class NTDSParserConsole:
	def __init__(self, bootkey, ntdsfile, ignore_errors = True, with_history = True):
		self.bootkey = bootkey
		self.ntdsfile = ntdsfile
		self.ignore_errors = ignore_errors
		self.with_history = with_history
		self.__sids = {}

	async def get_total_rows(self, max_rows = None):
		logger.debug('Fetching total row count...')
		file = self.ntdsfile
		if isinstance(self.ntdsfile, str):
			file = AFile(self.ntdsfile)

		db = ESENT_DB(file)
		_, err = await db.parse()
		if err is not None:
			raise err
			
		total = 1
		total, err = await db.get_rowcnt('datatable', max_rows = max_rows)
		if err is not None:
			raise err

		logger.debug('Total row count done! %s' % total)
		return total

	async def get_secrets(self):
		try:
			hexkey = False
			if isinstance(self.bootkey, str) and len(self.bootkey) == 32:
				try:
					bootkey = bytes.fromhex(self.bootkey)
					hexkey = True
				except:
					pass
			
			if hexkey is False:
				regfile = self.bootkey
				if isinstance(self.bootkey, str):
					regfile = AFile(self.bootkey)
				reghive = AIOWinRegHive(regfile)
				syshive = SYSTEM(reghive)
				bootkey = await syshive.get_bootkey()
			
			file = self.ntdsfile
			if isinstance(self.ntdsfile, str):
				file = AFile(self.ntdsfile)
			
			db = ESENT_DB(file)
			_, err = await db.parse()
			if err is not None:
				raise err
			
			ntds = NTDS(db, bootkey)			
			logger.debug('Dumping secrets')
			async for secret, err in ntds.dump_secrets(with_history=self.with_history, ignore_errors = self.ignore_errors):
				if secret is not None and err is None:
					if secret.object_sid not in self.__sids:
						self.__sids[secret.object_sid] = True
					else:
						raise Exception('Duplicate SID found!')
				yield secret, err
			
		except Exception as e:
			yield None, e

async def flush_buffer(buffer, outfile_handle = None, as_json = False):
	if as_json is True:
		return await flush_buffer_json(buffer, outfile_handle)
	else:
		try:
			if outfile_handle is not None:
				res = ''
				for secret in buffer:
					try:
						res += str(secret)
					except:
						continue
				outfile_handle.write(res)
			else:
				for secret in buffer:
					try:
						print(str(secret))
					except:
						continue
			
			buffer = []
			return True, None
		except Exception as e:
			return None, e

async def flush_buffer_json(buffer, outfile_handle = None):
	try:
		if outfile_handle is not None:
			res = []
			for secret in buffer:
				res.append(json.dumps(secret.to_dict()))
			outfile_handle.write('\r\n'.join(res))
		else:
			for secret in buffer:
				try:
					print(json.dumps(secret.to_dict()))
				except:
					continue
		return True, None
	except Exception as e:
		return None, e

async def amain():
	import argparse
	import traceback
	try:
		parser = argparse.ArgumentParser(description='NTDS.dit parser')
		parser.add_argument('-v', '--verbose', action='count', default=0)
		parser.add_argument('-p', '--progress', action='store_true', help='Show progress bar')
		parser.add_argument('-o', '--out-file', help='Output file path.')
		parser.add_argument('--json', action='store_true', help='Output in JSON format')
		parser.add_argument('--strict', action='store_true', help='Strict parsing. Fails on errors')
		parser.add_argument('--no-history', action='store_true', help='Do not parse history')
		parser.add_argument('bootkey',  help='Bootkey OR path to the SYSTEM hive file')
		parser.add_argument('ntdsfile', help='NTDS.dit file path')

		args = parser.parse_args()


		max_count = None

		ntdscon = NTDSParserConsole(
			args.bootkey,
			args.ntdsfile,
			ignore_errors=args.strict,
			with_history=not args.no_history
		)

		buffer = []
		buffer_size = 1000
		total = await ntdscon.get_total_rows(max_rows = max_count)
		if total == max_count:
			print('Stopped counting total rows at %s (that\'s a huge DB over there, congrats). Progress bar will not be accurate.' % max_count)

		if args.progress is True:
			pbar     = tqdm(desc='JET table parsing ', total=total, unit='records', miniters= total//200 ,position=0)
			pbar_sec = tqdm(desc='User secrets found', unit = '', miniters=buffer_size//10 ,position=1)

		outfile_handle = None
		if args.out_file is not None:
			outfile_handle = open(args.out_file, 'w', newline = '')
		
		async for secret, err in ntdscon.get_secrets():
			if err is not None:
				raise err

			if args.progress is True:
				pbar.update()
				
			if secret is None:
				continue
				
			if args.progress is True:
				pbar_sec.update()
			
			buffer.append(secret)
			if len(buffer) > buffer_size:
				_, err = await flush_buffer(buffer, outfile_handle, as_json = args.json)
				buffer = []
				if err is not None:
					raise err

			
		_, err = await flush_buffer(buffer, outfile_handle, as_json = args.json)
		buffer = []
		if err is not None:
			raise err
			
		
	except Exception as e:
		traceback.print_exc()


def main():
	asyncio.run(amain())

if __name__ == '__main__':
	main()
	