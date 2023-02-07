import pathlib
from aesedb.security.ntds import NTDS
from aesedb.eesentdb import ESENT_DB
from aesedb.utils.afile import AFile
from aesedb.security.ntds import NTDS
from aesedb.utils.systemhive import SYSTEM
from aiowinreg.ahive import AIOWinRegHive
import pytest
import asyncio



CURRENT_FILE_PATH = pathlib.Path(__file__).parent.absolute()
TESTDATA_DIR = CURRENT_FILE_PATH.joinpath('testdata')

async def parse_ntds(system_fname, ntds_fname):
	try:
		regfile = AFile(system_fname)
		reghive = AIOWinRegHive(regfile)
		syshive = SYSTEM(reghive)
		print('Getting bootkey...')
		bootkey = await syshive.get_bootkey()
		print('Bootkey: %s' % bootkey.hex())
		file = AFile(ntds_fname)
		
		print('Parsing ESENT DB...')
		db = ESENT_DB(file)
		_, err = await db.parse()
		if err is not None:
			raise err
		
		print('Getting total row count...')
		total, err = await db.get_rowcnt('datatable')
		if err is not None:
			raise err

		print('Dumping secrets...')
		secrets = []
		ntds = NTDS(db, bootkey)
		
		found_admin = False
		found_test2 = False
		found_krbtgt = False
		async for secret, err in ntds.dump_secrets(with_history=True, ignore_errors = False):
			if err is not None:
				raise err
			if secret is None:
				continue
			secrets.append(secret)
			if found_admin is False:
				if str(secret).find('Administrator') != -1:
					found_admin = True
			if found_test2 is False:
				if str(secret).find('test2') != -1:
					found_test2 = True
			if found_krbtgt is False:
				if str(secret).find('krbtgt') != -1:
					found_krbtgt = True

		if found_admin is False:
			raise Exception('Administrator not found')
		if found_test2 is False:
			raise Exception('test2 not found')
		if found_krbtgt is False:
			raise Exception('krbtgt not found')
		return secrets, None
	except Exception as e:
		return None, e

#@pytest.mark.asyncio
#async def test_2008_64():
#	ntds_fname = TESTDATA_DIR.joinpath('win2008_32', 'ntds.dit')
#	system_fname = TESTDATA_DIR.joinpath('win2008_32', 'SYSTEM')
#	res, err = await parse_ntds(system_fname, ntds_fname)
#	assert res is None

@pytest.mark.asyncio
async def test_2008r2_64():
	ntds_fname = TESTDATA_DIR.joinpath('win2008r2_64', 'ntds.dit')
	system_fname = TESTDATA_DIR.joinpath('win2008r2_64', 'SYSTEM')
	secrets, err = await parse_ntds(system_fname, ntds_fname)
	assert err is None
	assert len(secrets) > 0

@pytest.mark.asyncio
async def test_2012_64():
	ntds_fname = TESTDATA_DIR.joinpath('win2012_64', 'ntds.dit')
	system_fname = TESTDATA_DIR.joinpath('win2012_64', 'SYSTEM')
	secrets, err = await parse_ntds(system_fname, ntds_fname)
	assert err is None
	assert len(secrets) > 0

@pytest.mark.asyncio
async def test_2016_64():
	ntds_fname = TESTDATA_DIR.joinpath('win2016_64', 'ntds.dit')
	system_fname = TESTDATA_DIR.joinpath('win2016_64', 'SYSTEM')
	secrets, err = await parse_ntds(system_fname, ntds_fname)
	assert err is None
	assert len(secrets) > 0

@pytest.mark.asyncio
async def test_2019_64():
	ntds_fname = TESTDATA_DIR.joinpath('win2019_64', 'ntds.dit')
	system_fname = TESTDATA_DIR.joinpath('win2019_64', 'SYSTEM')
	secrets, err = await parse_ntds(system_fname, ntds_fname)
	assert err is None
	assert len(secrets) > 0

@pytest.mark.asyncio
async def test_2022_64():
	ntds_fname = TESTDATA_DIR.joinpath('win2022_64', 'ntds.dit')
	system_fname = TESTDATA_DIR.joinpath('win2022_64', 'SYSTEM')
	secrets, err = await parse_ntds(system_fname, ntds_fname)
	assert err is None
	assert len(secrets) > 0

@pytest.mark.asyncio
async def test_2019_64_clear():
	ntds_fname = TESTDATA_DIR.joinpath('win2019_64_clear', 'ntds.dit')
	system_fname = TESTDATA_DIR.joinpath('win2019_64_clear', 'SYSTEM')
	secrets, err = await parse_ntds(system_fname, ntds_fname)
	assert err is None
	assert len(secrets) > 0

if __name__ == '__main__':
	asyncio.run(test_2012_64())
