from setuptools import setup, find_packages
import re

VERSIONFILE="aesedb/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
	# Application name:
	name="aesedb",

	# Version number (initial):
	version=verstr,

	# Application author details:
	author="Tamas Jos",
	author_email="info@skelsecprojects.com",

	# Packages
	packages=find_packages(),

	# Include additional files into the package
	include_package_data=True,


	# Details
	url="https://github.com/skelsec/aesedb",

	zip_safe=True,
	#
	# license="LICENSE.txt",
	description="NTDS parser toolkit",

	# long_description=open("README.txt").read(),
	python_requires='>=3.6',
	classifiers=[
		"Programming Language :: Python :: 3.6",
		"Operating System :: OS Independent",
	],
	
	## these are only necessary for the command line tool
	## lib can work without additional deps
	install_requires=[
		'aiowinreg>=0.0.7',
		'tqdm',
		'colorama',
		'pycryptodomex',
	],

	entry_points={
		'console_scripts': [
			'antdsparse = aesedb.examples.ntdsparse:main',
		],
	}
)