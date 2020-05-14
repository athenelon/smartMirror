from source.newsApp.readUi import *
from source.newsApp.story import story

from source.extra.qtBasics import qtBasics
from source.extra.fileIO import fileIO

class readApp( qtBasics, readUi ):
	__fileIO = fileIO( )
	__story = []
	__sepa = ";~sepa~;"
	quitSignalExit = QtCore.pyqtSignal( int )

	def __init__( self, x, y, columnCount ):
		readUi.__init__( self, x, y, columnCount )
		qtBasics.__init__( self )
		
	def initUi( self, xPos, yPos ):
		self.move( xPos, yPos )
		self.tableWidget.itemDoubleClicked.connect( self.openLink )
		self.tableWidget.setRowCount( 0 )

	def addStoryToTable( self, singleStory ):
		numOfRows = self.tableWidget.rowCount( )
		qtStory = QTableWidgetItem( singleStory.getTitle( ))

		self.tableWidget.insertRow( numOfRows )
		self.tableWidget.setItem( numOfRows, 0, qtStory )

	def fillTable( self, file ):
		self.__story = []
		self.tableWidget.setRowCount( 0 )
		for i, singleStory in enumerate( self.__fileIO.simpleRead( file, multiLine=True, separator=self.__sepa )):
			self.__story.append( story( singleStory[0], singleStory[1] ))
			self.addStoryToTable( self.__story[i] )

	def openLink( self, item ):
		self.__story[item.row( )].openLink( )
