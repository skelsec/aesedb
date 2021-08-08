import io
from aesedb.structures.jetsignature import ESENT_JET_SIGNATURE

class ESENT_DB_HEADER:
	def __init__(self):
		self.CheckSum = None
		self.Signature = None
		self.Version= None
		self.FileType= None
		self.DBTime= None
		self.DBSignature= None
		self.DBState= None
		self.ConsistentPosition= None
		self.ConsistentTime= None
		self.AttachTime= None
		self.AttachPosition= None
		self.DetachTime= None
		self.DetachPosition= None
		self.LogSignature= None
		self.Unknown= None
		self.PreviousBackup= None
		self.PreviousIncBackup= None
		self.CurrentFullBackup= None
		self.ShadowingDisables= None
		self.LastObjectID= None
		self.WindowsMajorVersion= None
		self.WindowsMinorVersion= None
		self.WindowsBuildNumber= None
		self.WindowsServicePackNumber= None
		self.FileFormatRevision= None
		self.PageSize= None
		self.RepairCount= None
		self.RepairTime= None
		self.Unknown2= None
		self.ScrubTime= None
		self.RequiredLog= None
		self.UpgradeExchangeFormat= None
		self.UpgradeFreePages= None
		self.UpgradeSpaceMapPages= None
		self.CurrentShadowBackup= None
		self.CreationFileFormatVersion= None
		self.CreationFileFormatRevision= None
		self.Unknown3= None
		self.OldRepairCount= None
		self.ECCCount= None
		self.LastECCTime= None
		self.OldECCFixSuccessCount= None
		self.ECCFixErrorCount= None
		self.LastECCFixErrorTime= None
		self.OldECCFixErrorCount= None
		self.BadCheckSumErrorCount= None
		self.LastBadCheckSumTime= None
		self.OldCheckSumErrorCount= None
		self.CommittedLog= None
		self.PreviousShadowCopy= None
		self.PreviousDifferentialBackup= None
		self.Unknown4= None
		self.NLSMajorVersion= None
		self.NLSMinorVersion= None
		self.Unknown5= None
		self.UnknownFlags= None

	
	@staticmethod
	def from_bytes(data):
		return ESENT_DB_HEADER.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_DB_HEADER()
		res.CheckSum = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Signature = buff.read(4)
		res.Version = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.FileType = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.DBTime = int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.DBSignature = ESENT_JET_SIGNATURE.from_buffer(buff)
		res.DBState = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.ConsistentPosition= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.ConsistentTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.AttachTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.AttachPosition= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.DetachTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.DetachPosition= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.LogSignature= ESENT_JET_SIGNATURE.from_buffer(buff)
		res.Unknown= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.PreviousBackup= buff.read(24)
		res.PreviousIncBackup= buff.read(24)
		res.CurrentFullBackup= buff.read(24)
		res.ShadowingDisables= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.LastObjectID = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.WindowsMajorVersion= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.WindowsMinorVersion= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.WindowsBuildNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.WindowsServicePackNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.FileFormatRevision= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.PageSize = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.RepairCount= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.RepairTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.Unknown2= buff.read(28)
		res.ScrubTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.RequiredLog= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.UpgradeExchangeFormat= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.UpgradeFreePages= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.UpgradeSpaceMapPages= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.CurrentShadowBackup= buff.read(24)
		res.CreationFileFormatVersion= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.CreationFileFormatRevision= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Unknown3= buff.read(16)
		res.OldRepairCount= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.ECCCount= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.LastECCTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.OldECCFixSuccessCount= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.ECCFixErrorCount= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.LastECCFixErrorTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.OldECCFixErrorCount= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.BadCheckSumErrorCount= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.LastBadCheckSumTime= int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.OldCheckSumErrorCount= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.CommittedLog= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.PreviousShadowCopy= buff.read(24)
		res.PreviousDifferentialBackup= buff.read(24)
		res.Unknown4= buff.read(40)
		res.NLSMajorVersion= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.NLSMinorVersion= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Unknown5= buff.read(148)
		res.UnknownFlags= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		return res
	
	def __str__(self) -> str:
		t = ''
		for k in self.__dict__:
			t += '%s : %s\r\n' % (k, self.__dict__[k])
		return t