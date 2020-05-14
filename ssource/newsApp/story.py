from source.extra.fileIO import fileIO
import webbrowser

class story:
	__sepa = ";~sepa~;"
	__fileIO = fileIO( )

	def __init__( self, link, title ):
		self.__link = link
		self.__title = title

	def getLink( self ):
		return self.__link
	def getTitle( self ):
		return self.__title

	def setLink( self, link ):
		self.__link = link
	def setTitle( self, title ):
		self.__title = title

	def writeToFile( self, file ):
		self.__fileIO.simpleWrite( file, self.__link + self.__sepa + self.__title,
							  newLine=True, clearContents=False )

	def openLink( self ):
		webbrowser.open( self.__link )