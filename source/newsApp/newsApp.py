from source.newsApp.newsUi import newsUi, QtCore, QtWidgets
from source.newsApp.checkBoxHandler import checkBoxHandler
from source.newsApp.newsApiHandler import newsApiHandler
from source.newsApp.country import country
from source.extra.qtBasics import qtBasics
from source.extra.fileIO import fileIO

class newsApp( qtBasics, newsUi ):
	quitSignalAccept = QtCore.pyqtSignal( int )
	quitSignalCancel = QtCore.pyqtSignal( int )
	quitSignalExit = QtCore.pyqtSignal( int )

	__countryFile = "data/news/countryFile.txt"
	__sourcesFile = "data/news/sorucesFile.txt"
	__categoryFile = "data/news/categoryFile.txt"
	__newsStoryFile = "data/news/newsStory.txt"

	__fileIO = fileIO( )

	def __init__( self, x, y, sourceCount  ): #367, 259 xy
		newsUi.__init__( self, x, y, sourceCount )
		qtBasics.__init__( self )

		self.__category = checkBoxHandler( self.allCheckBox, self.categoryCheckBox )
		self.__source = checkBoxHandler( self.allCheckBox2, self.sourceCheckBox )

		self.__country = country( self.comboBox )

		self.__apinews = newsApiHandler( self.progressBar )

	def initUi( self ): 
		#Connect
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect( self.applyClicked )
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect( self.cancelClicked )

		self.__country.getCountryBox( ).currentIndexChanged.connect( self.countryChange )
		self.__country.setID( )
		self.countryChange( )

		self.__country.readFromFile( self.__countryFile )
		self.__category.readCheckedFromFile( self.__categoryFile )
		self.__source.readCheckedFromFile( self.__sourcesFile )

	def applyClicked( self ):
		self.buttonBox.hide( )

		self.__apinews.newNewsRequest( self.__newsStoryFile )
		self.__category.writeCheckedToFile( self.__categoryFile )
		self.__source.writeCheckedToFile( self.__sourcesFile )
		self.__country.writeToFile( self.__countryFile )

		categoryNames = self.__category.getCheckBoxNames( )
		sourceNames = self.__source.getCheckBoxNames( )
		if( len( categoryNames ) > 0 ):
			self.__apinews.pullCategory( categoryNames )
			self.__apinews.shuffleStory( )
			self.__apinews.writeToFile( self.__newsStoryFile )

		elif( len( sourceNames ) > 0 ):
			self.__apinews.pullSource( sourceNames )
			self.__apinews.shuffleStory( )
			self.__apinews.writeToFile( self.__newsStoryFile )

		self.buttonBox.show( )

		self.quitSignalAccept.emit( 1 )
		self.setVisible( False )

	def cancelClicked( self ):
		self.quitSignalCancel.emit( 1 )
		self.setVisible( False )

	def countryChange( self ):
		sourceNames = []
		self.__apinews.setCountryID( self.__country.getID( ))
		for names in self.__apinews.pullSourceNames( ):
			sourceNames.append( names['id'] )
		
		if( len( sourceNames )):
			self.label_2.hide( )# no sources available label
		else:
			self.label_2.show( )

		self.__source.changeCheckBox( sourceNames )

	def setCountryName( self ):#call this in applyClicked
		self.__country.writeToFile( self.__countryFile )

	def refresh( self ):
		self.__country.readFromFile( self.__countryFile )
		self.__source.readCheckedFromFile( self.__sourcesFile )