from source.extra.fileIO import fileIO

class newsList:
	__separator = ";~sepa~;"
	__fileIO = fileIO( )

	def __init__( self, label, table1, table2 ):
		self.__sources = table1
		self.__category = table2
		self.__country = label

	def updateTables( self, sourceFile, categoryFile ):
		self.updateList( sourceFile, self.__category )
		self.updateList( categoryFile, self.__sources )

	def updateList( self, file, qtList ):
		qtList.clear( )
		for item in self.__fileIO.simpleRead( file, multiLine=True ):
			qtList.addItem( item )

	def updateCountry( self, countryFile ):
		self.__country.setText( self.__fileIO.simpleRead( countryFile, separator=self.__separator )[0] )