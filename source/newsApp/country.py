from source.extra.fileIO import fileIO
from PyQt5 import QtCore

class country:
	__sepa = ";~sepa~;"
	__fileIO = fileIO( )

	__country = None
	__ID = ''

	__listOfIDs = ['ww', 'rs', 'gb', 'us', 'ru', 'gr', 'ch'] # ww-world wide

	__listOfCountryNames = ['World Wide', 'Serbia', 'United Kingdom',
							'United States', 'Russia', 'Greece', 'China']

	def __init__( self, country ):
		self.__country = country
		self.__ID = self.__listOfIDs[self.__country.currentIndex( )]

		self.__country.currentIndexChanged.connect( self.setID )

	def setID( self ):
		self.__ID = self.__listOfIDs[self.__country.currentIndex( )]

	def getID( self ):
		return self.__ID

	def getCountryName( self ):
		return self.__country.itemText( self.__country.currentIndex( ))

	def getCountryBox( self ):
		return self.__country ;

	def writeToFile( self, file ):
		self.__fileIO.simpleWrite( file, self.getCountryName( ) + self.__sepa + self.__ID  )

	def readFromFile( self, file ):
		name = self.__fileIO.simpleRead( file, separator=self.__sepa )[0]
		self.__country.setCurrentIndex( self.__country.findText( name ))
