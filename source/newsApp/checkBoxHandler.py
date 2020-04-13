from source.extra.fileIO import fileIO

class checkBoxHandler:
	__allCheckBox = None
	__checkBox = []
	__fileIO = fileIO( )
	__numOfChecked = 0

	def __init__( self, allCheckBox, checkBox ):
		self.__allCheckBox = allCheckBox
		self.__checkBox = checkBox

		self.__allCheckBox.clicked.connect( self.setAllCheckBoxState )
		for i in range( len( self.__checkBox )):
			self.__checkBox[i].clicked.connect( lambda _, box=self.__checkBox[i]: self.setCheckBoxState( box ))

	def getCheckBoxLen( self ):
		cbLen = 0
		for box in self.__checkBox:
			if( len( box.text( ))):
				cbLen += 1
		print( cbLen, " LEN")
		return cbLen

	def getCheckBoxNames( self ):
		selected = []
		for checkBox in self.__checkBox:
			if( checkBox.isChecked( )):
				selected.append( checkBox.text( ))
		return selected


	def setCheckBoxName( self, index, name ):
		self.__checkBox[index].setText( name )

	def setCheckBoxState( self, checkBox ):
		if( checkBox.isChecked( )):
			self.__numOfChecked += 1
		else:
			self.__numOfChecked -= 1
		self.checkTriState( )

	def setAllCheckBoxState( self ):
		state = self.__allCheckBox.isChecked( )
		if( state == 1 ):#Dont want tri state from click
			state = 2
			self.__allCheckBox.setCheckState( state )

		if( state == 2 or state == 0 ):
			for checkBox in self.__checkBox:
				checkBox.setChecked( state )
			if( state ):
				self.__numOfChecked = self.getCheckBoxLen( )
			else:
				self.__numOfChecked = 0

	def checkTriState( self ):
		state = 0 # false
		if( self.__numOfChecked == self.getCheckBoxLen( )):
			state = 2 # true
		elif( self.__numOfChecked > 0 and self.__numOfChecked < self.getCheckBoxLen( )):
			state = 1 # tri
		self.setTriState( state )

	def setTriState( self, state ):# 0-false 1-triState 2-True
		self.__allCheckBox.setCheckState( state )

	def checkIfSet( self, index ):
		return self.__checkBox[index].isChecked( )

	def changeCheckBox( self, listOfNewText ):
		for checkBox in self.__checkBox:
			checkBox.hide( )
			checkBox.setText( "" )
			checkBox.setChecked( False )

		for i, text in enumerate( listOfNewText ):
			self.__checkBox[i].setText( text )
			self.__checkBox[i].show( )
			self.__numOfChecked = i

		self.setTriState( False )

	def writeCheckedToFile( self, file ):
		self.__fileIO.conditionalQtWrite( file, self.__checkBox, newLine=True, clearContents=True )

	def readCheckedFromFile( self, file ):
		self.__numOfChecked = self.__fileIO.conditionalQtRead( file, self.__checkBox )
		print( self.__numOfChecked )
		self.checkTriState( )