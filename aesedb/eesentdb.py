from aesedb.security.constants import INTERNAL_TO_NAME, NAME_TO_ATTRTYP
from collections import OrderedDict
import enum
from struct import unpack

from aesedb.structures.header import ESENT_DB_HEADER
from aesedb.structures.page import ESENT_PAGE, PAGEFLAGS, WELLKNOWNPAGENO
from aesedb.structures.branchentry import readbranchentry
from aesedb.structures.leafentry import readleafentry
from aesedb.structures.datadefinitionheader import ESENT_DATA_DEFINITION_HEADER
from aesedb.structures.catalogdatadefentry import ESENT_CATALOG_DATA_DEFINITION_ENTRY, CATALOG_TYPE


TABLE_CURSOR = {
	'TableData' : b'',
	'FatherDataPageNumber': 0,
	'CurrentPageData' : b'',
	'CurrentTag' : 0,
}

# Tagged Data Type Flags
class TAGGED_DATA_TYPE(enum.IntFlag):
	VARIABLE_SIZE = 1
	COMPRESSED    = 2
	STORED        = 4
	MULTI_VALUE   = 8
	WHO_KNOWS     = 10

# Column Types
JET_coltypNil          = 0
JET_coltypBit          = 1
JET_coltypUnsignedByte = 2
JET_coltypShort        = 3
JET_coltypLong         = 4
JET_coltypCurrency     = 5
JET_coltypIEEESingle   = 6
JET_coltypIEEEDouble   = 7
JET_coltypDateTime     = 8
JET_coltypBinary       = 9
JET_coltypText         = 10
JET_coltypLongBinary   = 11
JET_coltypLongText     = 12
JET_coltypSLV          = 13
JET_coltypUnsignedLong = 14
JET_coltypLongLong     = 15
JET_coltypGUID         = 16
JET_coltypUnsignedShort= 17
JET_coltypMax          = 18

ColumnTypeSize = {
    JET_coltypNil          : None,
    JET_coltypBit          : (1,'B'),
    JET_coltypUnsignedByte : (1,'B'),
    JET_coltypShort        : (2,'<h'),
    JET_coltypLong         : (4,'<l'),
    JET_coltypCurrency     : (8,'<Q'),
    JET_coltypIEEESingle   : (4,'<f'),
    JET_coltypIEEEDouble   : (8,'<d'),
    JET_coltypDateTime     : (8,'<Q'),
    JET_coltypBinary       : None,
    JET_coltypText         : None, 
    JET_coltypLongBinary   : None,
    JET_coltypLongText     : None,
    JET_coltypSLV          : None,
    JET_coltypUnsignedLong : (4,'<L'),
    JET_coltypLongLong     : (8,'<Q'),
    JET_coltypGUID         : (16,'16s'),
    JET_coltypUnsignedShort: (2,'<H'),
    JET_coltypMax          : None,
}

# Code pages
CODEPAGE_UNICODE = 1200
CODEPAGE_ASCII   = 20127
CODEPAGE_WESTERN = 1252

StringCodePages = {
    CODEPAGE_UNICODE : 'utf-16le', 
    CODEPAGE_ASCII   : 'ascii',
    CODEPAGE_WESTERN : 'cp1252',
}

class ESENT_DB:
	def __init__(self, dbfile, pageSize = 8192):
		self.__pageSize = pageSize
		self.__DB = dbfile
		self.__DBHeader = None
		self.__totalPages = None
		self.__tables = OrderedDict()
		self.__currentTable = None
	
	async def parse(self):
		try:
			mainHeader, err = await self.get_page(-1)
			if err is not None:
				raise err
			self.__DBHeader = ESENT_DB_HEADER.from_bytes(mainHeader)
			#print(self.__DBHeader)
			self.__pageSize = self.__DBHeader.PageSize
			await self.__DB.seek(0,2)
			self.__totalPages = (self.__DB.tell() // self.__pageSize) -2
			#print("Database Version:0x%x, Revision:0x%x"% (self.__DBHeader.Version, self.__DBHeader.FileFormatRevision))
			#print("Page Size: %d" % self.__pageSize)
			#print("Total Pages in file: %d" % self.__totalPages)
			_, err = await self.parse_catalog(WELLKNOWNPAGENO.CATALOG.value)
			if err is not None:
				raise err

			return True, None
		except Exception as e:
			return None, e
	
	async def get_page(self, pageno, force_parse = False):
		try:
			#print("Trying to fetch page %d (0x%x)" % (pageno, (pageno+1)*self.__pageSize))
			await self.__DB.seek((pageno+1)*self.__pageSize, 0)
			data = await self.__DB.read(self.__pageSize)
			while len(data) < self.__pageSize:
				remaining = self.__pageSize - len(data)
				t = await self.__DB.read(remaining)
				data += t
			# Special case for the first page
			if pageno <= 0 and force_parse is False:
				return data, None
			
			page = ESENT_PAGE(self.__DBHeader)
			_, err = await page.read(data)
			if err is not None:
				raise err
			#print(page)
			return page, None
		except Exception as e:
			return None, e
		
	
	async def parse_catalog(self, pageno):
		try:
			page, err = await self.get_page(pageno)
			if err is not None:
				raise err
			_, err = await self.parse_page(page)
			if err is not None:
				raise err

			for i in range(1, page.record.FirstAvailablePageTag):
				flags, data = page.get_tag(i)
				if page.record.PageFlags & PAGEFLAGS.LEAF == 0:
					# Branch page
					branchEntry, err = await readbranchentry(flags, data)
					if err is not None:
						raise err
						
					_, err = await self.parse_catalog(branchEntry.ChildPageNumber)
					if err is not None:
						raise err
			return True, None
		except Exception as e:
			return None, e
	
	async def parse_page(self, page):
		try:
			for tagno in range(1,page.record.FirstAvailablePageTag):
				flags, data = page.get_tag(tagno)
				if page.record.PageFlags & PAGEFLAGS.LEAF > 0:
					# Leaf page
					if page.record.PageFlags & PAGEFLAGS.SPACE_TREE > 0:
						pass
					elif page.record.PageFlags & PAGEFLAGS.INDEX > 0:
						pass
					elif page.record.PageFlags & PAGEFLAGS.LONG_VALUE > 0:
						pass
					else:
						le, err = await readleafentry(flags, data)
						if err is not None:
							raise err
						self.__addItem(le)
						
					

			return True, None
		except Exception as e:
			return None, e

	def __parseItemName(self,entry):
		dataDefinitionHeader = ESENT_DATA_DEFINITION_HEADER.from_bytes(entry.EntryData)

		if dataDefinitionHeader.LastVariableDataType > 127:
			numEntries =  dataDefinitionHeader.LastVariableDataType - 127
		else:
			numEntries =  dataDefinitionHeader.LastVariableDataType

		itemLen = int.from_bytes(entry.EntryData[dataDefinitionHeader.VariableSizeOffset:][:2], byteorder='little', signed=False)
		itemName = entry.EntryData[dataDefinitionHeader.VariableSizeOffset:][2*numEntries:][:itemLen]
		return itemName

	def __addItem(self, entry):
		dataDefinitionHeader = ESENT_DATA_DEFINITION_HEADER.from_bytes(entry.EntryData)
		catalogEntry = ESENT_CATALOG_DATA_DEFINITION_ENTRY.from_bytes(entry.EntryData[dataDefinitionHeader._len:])
		itemName = self.__parseItemName(entry)

		if catalogEntry.Type == CATALOG_TYPE.TABLE:
			self.__tables[itemName] = OrderedDict()
			self.__tables[itemName].TableEntry = entry
			self.__tables[itemName].Columns    = OrderedDict()
			self.__tables[itemName].Indexes    = OrderedDict()
			self.__tables[itemName].LongValues = OrderedDict()
			self.__currentTable = itemName
		elif catalogEntry.Type == CATALOG_TYPE.COLUMN:
			self.__tables[self.__currentTable].Columns[itemName] = entry
			self.__tables[self.__currentTable].Columns[itemName].Header = dataDefinitionHeader
			self.__tables[self.__currentTable].Columns[itemName].Record = catalogEntry
		elif catalogEntry.Type == CATALOG_TYPE.INDEX:
			self.__tables[self.__currentTable].Indexes[itemName] = entry
		elif catalogEntry.Type == CATALOG_TYPE.LONG_VALUE:
			self.__addLongValue(entry)
		else:
			raise Exception('Unknown type 0x%x' % catalogEntry['Type'])

	def __addLongValue(self, entry):
		dataDefinitionHeader = ESENT_DATA_DEFINITION_HEADER.from_bytes(entry.EntryData)
		lvLen = int.from_bytes(entry.EntryData[dataDefinitionHeader.VariableSizeOffset:][:2], byteorder='little', signed=False)
		lvName = entry.EntryData[dataDefinitionHeader.VariableSizeOffset:][7:][:lvLen]
		self.__tables[self.__currentTable].LongValues[lvName] = entry

	async def open_table(self, tablename):
		try:
			# Returns a cursos for later use

			if isinstance(tablename, bytes) is not True:
				tablename = tablename.encode()

			if tablename in self.__tables:
				entry = self.__tables[tablename].TableEntry
				dataDefinitionHeader = ESENT_DATA_DEFINITION_HEADER.from_bytes(entry.EntryData)
				catalogEntry = ESENT_CATALOG_DATA_DEFINITION_ENTRY.from_bytes(entry.EntryData[dataDefinitionHeader._len:])
				
				# Let's position the cursor at the leaf levels for fast reading
				pageNum = catalogEntry.FatherDataPageNumber
				done = False
				while done is False:
					page, err = await self.get_page(pageNum)
					if err is not None:
						raise err
					
					if page.record.FirstAvailablePageTag <= 1:
						# There are no records
						done = True
					for i in range(1, page.record.FirstAvailablePageTag):
						flags, data = page.get_tag(i)
						if page.record.PageFlags & PAGEFLAGS.LEAF == 0:
							# Branch page, move on to the next page
							branchEntry, err = await readbranchentry(flags, data)
							if err is not None:
								raise err
							pageNum = branchEntry.ChildPageNumber
							break
						else:
							done = True
							break
					
				cursor = TABLE_CURSOR
				cursor['TableData'] = self.__tables[tablename]
				cursor['FatherDataPageNumber'] = catalogEntry.FatherDataPageNumber
				cursor['CurrentPageData'] = page
				cursor['CurrentTag']  = 0
				return cursor, None
			else:
				raise Exception('Table not found!')
		except Exception as e:
			return None, e

	async def __get_next_tag(self, cursor):
		try:
			page = cursor['CurrentPageData']

			if cursor['CurrentTag'] >= page.record.FirstAvailablePageTag:
				# No more data in this page, chau
				return None, None

			flags, data = page.get_tag(cursor['CurrentTag'])
			if page.record.PageFlags & PAGEFLAGS.LEAF > 0:
				# Leaf page
				if page.record.PageFlags & PAGEFLAGS.SPACE_TREE > 0:
					raise Exception('FLAGS_SPACE_TREE > 0')
				elif page.record.PageFlags & PAGEFLAGS.INDEX > 0:
					raise Exception('FLAGS_INDEX > 0')
				elif page.record.PageFlags & PAGEFLAGS.LONG_VALUE > 0:
					raise Exception('FLAGS_LONG_VALUE > 0')
				else:
					# Table Value
					leafEntry, err = await readleafentry(flags, data)
					if err is not None:
						raise err
					return leafEntry, None

			return None, None
		except Exception as e:
			return None, e

	async def get_rowcnt(self, table_name):
		try:
			cursor, err = await self.open_table(table_name)
			if err is not None:
				raise err
			
			ctr = 0
			while True:
				res, err = await self.__next_row_ctr(cursor)
				if err is not None:
					raise err
				if res is None:
					break
				ctr += 1
			
			return ctr, None

		except Exception as e:
			return None, e
	
	async def __next_row_ctr(self, cursor):
		try:
			cursor['CurrentTag'] += 1
			tag, err = await self.__get_next_tag(cursor)
			if err is not None:
				raise err
			
			if tag is None:
				# No more tags in this page, search for the next one on the right
				page = cursor['CurrentPageData']
				if page.record.NextPageNumber == 0:
					# No more pages, chau
					return None, None
				else:
					cursor['CurrentPageData'], err = await self.get_page(page.record.NextPageNumber)
					if err is not None:
						raise err
					cursor['CurrentTag'] = 0
					return await self.__next_row_ctr(cursor)
			return True, None
				

		except Exception as e:
			return None, e
	
	async def get_next_row(self, cursor, filter_col = None):
		try:
			cursor['CurrentTag'] += 1
			#print('currenttag %s ' %cursor['CurrentTag'])
			tag, err = await self.__get_next_tag(cursor)
			if err is not None:
				raise err
			#print(tag)

			if tag is None:
				# No more tags in this page, search for the next one on the right
				page = cursor['CurrentPageData']
				if page.record.NextPageNumber == 0:
					# No more pages, chau
					return None, None
				else:
					cursor['CurrentPageData'], err = await self.get_page(page.record.NextPageNumber)
					if err is not None:
						raise err
					cursor['CurrentTag'] = 0
					return await self.get_next_row(cursor, filter_col = filter_col)
			else:
				res, err = await self.__tag_to_record(cursor, tag.EntryData, filter_col)
				if err is not None:
					raise err
				return res, None
		
		except Exception as e:
			return None, e
	
	async def __tag_to_record(self, cursor, tag, filter_col:dict = None):
		try:
			record = OrderedDict()
			taggedItems = OrderedDict()
			taggedItemsParsed = False

			dataDefinitionHeader = ESENT_DATA_DEFINITION_HEADER.from_bytes(tag)
			#dataDefinitionHeader.dump()
			variableDataBytesProcessed = (dataDefinitionHeader.LastVariableDataType - 127) * 2
			prevItemLen = 0
			tagLen = len(tag)
			fixedSizeOffset = dataDefinitionHeader._len
			variableSizeOffset = dataDefinitionHeader.VariableSizeOffset 
	
			columns = cursor['TableData'].Columns

			prev_column_name = None
			prev_column_mandatory = False
			for column in list(columns.keys()):
				#input(column)
				#input(filter_col)
				#if prev_column_name is not None:
				#	if record[prev_column_name] is None and prev_column_mandatory is True:
				#		#if INTERNAL_TO_NAME[prev_column_name].lower() != 'peklist':
				#		#	print(INTERNAL_TO_NAME[prev_column_name])
				#		#	print(record[prev_column_name] is None)
				#		#	print(prev_column_mandatory is True)
				#		#	print('Mandatory field missing! Skipping record!')
				#		#	input()
				#		return OrderedDict(), None

				if filter_col is not None and column not in filter_col:
					#print('skipping')
					continue
				
				if filter_col is not None:
					prev_column_name = column
					prev_column_mandatory = bool(filter_col[column])

				columnRecord = columns[column].Record
				#columnRecord.dump()
				if columnRecord.Identifier <= dataDefinitionHeader.LastFixedSize:
					# Fixed Size column data type, still available data
					record[column] = tag[fixedSizeOffset:][:columnRecord.SpaceUsage]
					fixedSizeOffset += columnRecord.SpaceUsage

				elif 127 < columnRecord.Identifier <= dataDefinitionHeader.LastVariableDataType:
					# Variable data type
					index = columnRecord.Identifier - 127 - 1
					itemLen = int.from_bytes(tag[variableSizeOffset+index*2:][:2], byteorder='little', signed=False)

					if itemLen & 0x8000:
						# Empty item
						itemLen = prevItemLen
						record[column] = None
					else:
						itemValue = tag[variableSizeOffset+variableDataBytesProcessed:][:itemLen-prevItemLen]
						record[column] = itemValue

					#if columnRecord['Identifier'] <= dataDefinitionHeader['LastVariableDataType']:
					variableDataBytesProcessed +=itemLen-prevItemLen

					prevItemLen = itemLen

				elif columnRecord.Identifier > 255:
					# Have we parsed the tagged items already?
					if taggedItemsParsed is False and (variableDataBytesProcessed+variableSizeOffset) < tagLen:
						index = variableDataBytesProcessed+variableSizeOffset
						#hexdump(tag[index:])
						endOfVS = self.__pageSize
						firstOffsetTag = (int.from_bytes(tag[index+2:][:2], byteorder='little', signed=False) & 0x3fff) + variableDataBytesProcessed + variableSizeOffset
						while True:
							taggedIdentifier = int.from_bytes(tag[index:][:2], byteorder='little', signed=False)
							index += 2
							taggedOffset = int.from_bytes(tag[index:][:2], byteorder='little', signed=False) & 0x3fff 
							# As of Windows 7 and later ( version 0x620 revision 0x11) the 
							# tagged data type flags are always present
							if self.__DBHeader.Version == 0x620 and self.__DBHeader.FileFormatRevision >= 17 and self.__DBHeader.PageSize > 8192: 
								flagsPresent = 1
							else:
								flagsPresent = int.from_bytes(tag[index:][:2], byteorder='little', signed=False) & 0x4000
							index += 2
							if taggedOffset < endOfVS:
								endOfVS = taggedOffset
							taggedItems[taggedIdentifier] = (taggedOffset, tagLen, flagsPresent)
							#print "ID: %d, Offset:%d, firstOffset:%d, index:%d, flag: 0x%x" % (taggedIdentifier, taggedOffset,firstOffsetTag,index, flagsPresent)
							if index >= firstOffsetTag:
								# We reached the end of the variable size array
								break
					
						# Calculate length of variable items
						# Ugly.. should be redone
						prevKey = list(taggedItems.keys())[0]
						for i in range(1,len(taggedItems)):
							offset0, length, flags = taggedItems[prevKey]
							offset, _, _ = list(taggedItems.items())[i][1]
							taggedItems[prevKey] = (offset0, offset-offset0, flags)
							#print ("ID: %d, Offset: %d, Len: %d, flags: %d" % (prevKey, offset0, offset-offset0, flags))
							prevKey = list(taggedItems.keys())[i]
						taggedItemsParsed = True
	
					# Tagged data type
					if columnRecord.Identifier in taggedItems:
						offsetItem = variableDataBytesProcessed + variableSizeOffset + taggedItems[columnRecord.Identifier][0] 
						itemSize = taggedItems[columnRecord.Identifier][1]
						# If item have flags, we should skip them
						if taggedItems[columnRecord.Identifier][2] > 0:
							itemFlag = ord(tag[offsetItem:offsetItem+1])
							offsetItem += 1
							itemSize -= 1
						else:
							itemFlag = 0

						#print("ID: %d, itemFlag: 0x%x" %( columnRecord.Identifier, itemFlag))
						if itemFlag & TAGGED_DATA_TYPE.COMPRESSED:
							#print('Unsupported tag column: %s, flag:0x%x' % (column, itemFlag))
							record[column] = None
						elif itemFlag & TAGGED_DATA_TYPE.MULTI_VALUE:
							# ToDo: Parse multi-values properly
							#print('Multivalue detected in column %s, returning raw results' % (column))
							record[column] = (tag[offsetItem:][:itemSize],)
						else:
							record[column] = tag[offsetItem:][:itemSize]

					else:
						record[column] = None
				else:
					record[column] = None

				# If we understand the data type, we unpack it and cast it accordingly
				# otherwise, we just encode it in hex
				if type(record[column]) is tuple:
					# A multi value data, we won't decode it, just leave it this way
					record[column] = record[column][0]
				elif columnRecord.ColumnType == JET_coltypText or columnRecord.ColumnType == JET_coltypLongText: 
					# Let's handle strings
					if record[column] is not None:
						if columnRecord.CodePage not in StringCodePages:
							raise Exception('Unknown codepage 0x%x'% columnRecord['CodePage'])
						stringDecoder = StringCodePages[columnRecord.CodePage]

						try:
							record[column] = record[column].decode(stringDecoder)
						except Exception:
							#print("Exception:", exc_info=True)
							#print('Fixing Record[%r][%d]: %r' % (column, columnRecord['ColumnType'], record[column]))
							record[column] = record[column].decode(stringDecoder, "replace")
							pass
				else:
					unpackData = ColumnTypeSize[columnRecord.ColumnType]
					if record[column] is not None:
						if unpackData is None:
							record[column] = record[column]
						else:
							unpackStr = unpackData[1]
							record[column] = unpack(unpackStr, record[column])[0]

			return record, None

		except Exception as e:
			return None, e

