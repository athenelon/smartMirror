from source.extra.fileIO import fileIO

class event:
	__hour = "00"
	__minute = "00"

	__text = ""

	__fileIO = fileIO( )
	__separator = ";~sepa~;"

	def __init__( self, hour, minute, text ):
		self.__hour = str( hour )
		self.__minute = str( minute )
		self.__text = text

	def getTime( self ):
		return self.__hour + ":" + self.__minute

	def getText( self ):
		return self.__text

	def addLeadingZero( self ):
		if( len( self.__hour ) == 1 ):
			self.__hour = "0" + self.__hour

		if( len( self.__minute ) == 1 ):
			self.__minute = "0" + self.__minute

	def formatForFile( self ):
		self.addLeadingZero( )		
		return self.__hour + ":" + self.__minute + self.__separator + self.__text

	def formatForTable( self ):
		self.addLeadingZero( )
		return [ self.__hour + ":" + self.__minute, self.__text ]

	def writeToFile( self, file ):
		self.__fileIO.simpleWrite( file, self.formatForFile( ), newLine=True, clearContents=False )