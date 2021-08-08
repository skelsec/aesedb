import asyncio
from tqdm import tqdm
from aesedb.eesentdb import ESENT_DB
from aesedb.utils.afile import AFile
from aesedb.security.ntds import NTDS
from aesedb.utils.systemhive import SYSTEM
from aiowinreg.ahive import AIOWinRegHive
from aesedb import logger

class NTDSParserConsole:
	def __init__(self, bootkey, ntdsfile, show_progress = True, outfile = None, ext_result_q = None):
		self.bootkey = bootkey
		self.ntdsfile = ntdsfile
		self.show_progress = show_progress
		self.outfile = outfile
		self.ext_result_q = ext_result_q
		self.buffer_size = 100
		self.buffer = []

		self.outfile_handle = None
	
	async def flush_buffer(self):
		try:
			if self.outfile_handle is not None:
				res = ''
				for secret in self.buffer:
					res += str(secret)

				self.outfile_handle.write(res)

			else:
				for secret in self.buffer:			
					print(str(secret))
			
			self.buffer = []
			return True, None
		except Exception as e:
			return None, e

	async def run(self):
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

			logger.debug('Fetching total row count')
			total, err = await db.get_rowcnt('datatable')
			if err is not None:
				raise err
			
			ntds = NTDS(db, bootkey)
			if self.show_progress is True:
				pbar     = tqdm(desc='JET table parsing ', total=total, unit='records', miniters= total//200 ,position=0)
				pbar_sec = tqdm(desc='User secrets found', unit = '', miniters=self.buffer_size//10 ,position=1)

			if self.outfile is not None:
				self.outfile_handle = open(self.outfile, 'w', newline = '')
			
			logger.debug('Dumping secrets')
			async for secret, err in ntds.dump_secrets():
				if err is not None:
					raise err

				if self.show_progress is True:
					pbar.update()
				
				if self.ext_result_q is not None:
					await self.ext_result_q.put((secret, total, None, False)) # secret, total, error, end
				
				if secret is None:
					continue
				
				if self.show_progress is True:
					pbar_sec.update()
				
				if self.ext_result_q is None:
					self.buffer.append(secret)
					if len(self.buffer) > self.buffer_size:
						_, err = await self.flush_buffer()
						if err is not None:
							raise err

			if self.ext_result_q is None:
				_, err = await self.flush_buffer()
				if err is not None:
					raise err
			
			else:
				await self.ext_result_q.put((None, total, None, True))

			return True, None
		except Exception as e:
			if self.ext_result_q is not None:
				await self.ext_result_q.put((None, None, e, True)) # secret, error, end
			return None, e

def main():
	import argparse
	import traceback
	try:
		parser = argparse.ArgumentParser(description='NTDS.dit parser')
		parser.add_argument('-v', '--verbose', action='count', default=0)
		parser.add_argument('-p', '--progress', action='store_true', help='Show progress bar')
		parser.add_argument('-o', '--out-file', help='Output file path.')
		parser.add_argument('bootkey',  help='Bootkey OR path to the SYSTEM hive file')
		parser.add_argument('ntdsfile', help='NTDS.dit file path')

		args = parser.parse_args()

		ntdscon = NTDSParserConsole(
			args.bootkey,
			args.ntdsfile,
			show_progress = args.progress,
			outfile = args.out_file,
			ext_result_q = None
		)

		_, err = asyncio.run(ntdscon.run())
		if err is not None:
			raise err
	except Exception as e:
		traceback.print_exc()

if __name__ == '__main__':
	main()
	