from source.mainApp.ui import ui, QtWidgets, QColorDialog, QtGui
from source.newsApp.newsApp import newsApp
from source.newsApp.readApp import readApp
from source.mainApp.eventHandler import eventHandler
from source.mainApp.newsList import newsList

from source.extra.fileIO import fileIO
from source.extra.initFoldersAndFiles import initFoldersAndFiles
from source.client.client import socketClient

import threading

class app(ui):

	#__eventFile = "data/configFiles/eventFile.txt"
	__fontFile = "data/configFiles/fontFile.txt"
	__colorFile = "data/configFiles/colorFile.txt"
	__brightnessFile = "data/configFiles/brightnessFile.txt"
	__radioFile = "data/weather/radioFile.txt"
	__cityFile = "data/weather/cityFile.txt"
	__weatherFile = "data/weather/weather.txt"
	__dummyFile = "data/events/dummy.txt"
	__newsStoryFile = "data/news/newsStory.txt"
	__countryFile = "data/news/countryFile.txt"
	__sourcesFile = "data/news/sorucesFile.txt"
	__categoryFile = "data/news/categoryFile.txt"

	__fileIO = fileIO( )

	def __init__( self, x, y ):#x805, y573
		import sys
		self.app = QtWidgets.QApplication( sys.argv )
		super( ).__init__( x, y )

		self.initUi( )

		sys.exit( self.app.exec_( ))

	def initUi( self ):
		self.__socketClient = socketClient( '127.0.0.1', 8080 )

		self.__initFoldersAndFiles = initFoldersAndFiles( )
		self.__newsApp = newsApp( 367, 259, 200 )
		self.__readApp = readApp( 797, 392, 1 )
		self.__newsList = newsList( self.countryLabel, self.sourceListWidget, self.newsListWidget )
		self.__events = eventHandler( self.eventTableWidget, self.hourComboBox, self.minuteSpinBox, 
									  self.addEventButton, self.removeEventButton, self.lineEdit, self.dateLabel)

		self.__initFoldersAndFiles.initAllFolders( )
		self.__initFoldersAndFiles.initAllFiles( )

		self.__newsApp.initUi( )
		self.__readApp.initUi( super( ).x( ), super( ).y( ))

		self.__run_threads = True
		self.__thread = threading.Thread(target=self.__socketClient.checkIfConnected, args =(5, self.pingLabel, lambda : self.__run_threads, ))
		self.__thread.start( )

		#Move Main Window
		screenRes = QtWidgets.QDesktopWidget( ).screenGeometry(-1)

		moveX = screenRes.width( ) - self.width() - 40
		moveY = screenRes.height( ) - self.height() - 100

		

		self.setDate( )
		self.readFontAndSize( )
		self.readBrightness( )
		self.readColor( )
		self.readWeather( )
		
		self.connectWidgets( )
		super( ).move( moveX, moveY )
		super( ).setVisible( True )

	def connectWidgets( self ):
		self.__newsApp.quitSignalAccept.connect( self.updateNews )
		self.__newsApp.quitSignalCancel.connect( self.enableWindow )
		self.__newsApp.quitSignalExit.connect( self.enableWindow )
		self.__readApp.quitSignalExit.connect( self.enableWindow )

		#Font
		self.fontComboBox.currentFontChanged.connect( self.writeFontAndSize )
		self.fontSizeSpinBox.valueChanged.connect( self.writeFontAndSize )
		self.boldCheckBox.clicked.connect( self.writeFontAndSize )
		self.italicCheckBox.clicked.connect( self.writeFontAndSize )
		#
		self.colorChangeButton.clicked.connect( self.changeColor )
		self.calendarWidget.clicked.connect( self.setDate )
		self.brightnessSlider.sliderReleased.connect( self.writeBrightness )
		self.editNewsButton.clicked.connect( self.editNews )
		self.readNewsButton.clicked.connect( self.readNews )

		self.submitButton.clicked.connect( self.writeWeather )

	def writeFontAndSize( self ):
		self.__fileIO.conditionalWrite( self.__fontFile, 
									  self.__fileIO.formListOfDictionary([ True, True, self.boldCheckBox.isChecked( ), self.italicCheckBox.isChecked( )],
													 				   [ self.fontComboBox.currentFont( ).toString( ), self.fontSizeSpinBox.value( ), "Bold", "Italic" ]),
									  separator='\n' )
		self.sendToServer( self.__fontFile )

	def writeBrightness( self ):
		self.__fileIO.simpleWrite( self.__brightnessFile, str( self.brightnessSlider.value( )))
		self.sendToServer( self.__brightnessFile )

	def writeWeather( self ):
		self.__fileIO.conditionalQtWrite( self.__weatherFile, [self.celsiusRadioButton, self.fahrenheitRadioButton])
		self.__fileIO.simpleWrite( self.__weatherFile, "\n" + self.cityLineEdit.text( ), clearContents=False )
		self.sendToServer( self.__weatherFile )

	def writeColor( self, text ):
		self.__fileIO.simpleWrite( self.__colorFile, text )
		self.sendToServer( self.__colorFile )

	def readFontAndSize( self ):
		fontInit = self.__fileIO.conditionalQtRead( self.__fontFile, [ self.boldCheckBox, self.italicCheckBox ], returnText=True )
		self.fontComboBox.setCurrentFont( QtGui.QFont( fontInit[0] ))
		self.fontSizeSpinBox.setValue( int( fontInit[1] ))

	def readBrightness( self ):
		self.brightnessSlider.setValue( int( self.__fileIO.simpleRead( self.__brightnessFile, force=True )))

	def readWeather( self ):
		text = self.__fileIO.conditionalQtRead( self.__weatherFile, [ self.celsiusRadioButton, self.fahrenheitRadioButton ], force=True, returnText=True)
		self.cityLineEdit.setText( text[1] )

	def readColor( self ):
		self.colorChangeButton.setStyleSheet( "QWidget { background-color: %s ; color: %s }"% tuple( self.__fileIO.simpleRead( self.__colorFile, force=True, separator=":" )))

	def changeColor( self ):
		color = QColorDialog( ).getColor( )
		if color.isValid( ):
			r, g, b, _ = color.getRgb( )
			rgbHexa = '#%02x%02x%02x' % (abs( r - 255 ), abs( g - 255 ), abs( b - 255 ))
			self.colorChangeButton.setStyleSheet( "QWidget { background-color: %s ; color: %s }"% (color.name( ), rgbHexa))

			self.writeColor( color.name( ) + ":" + rgbHexa )

	def setDate( self ):
		dayOfWeek, month, day, year = self.calendarWidget.selectedDate( ).toString( ).split( " " )
		self.__events.setLabel( day + ". " + month + " " + year + ". (" + dayOfWeek + ")" )
		
		path = "data/events/" + str( year ) + "/" + str( month ) + "/" + day + ".txt"
		self.__events.setPath( path )

	def editNews( self ):
		self.setEnabled( False )
		self.__newsApp.refresh( )
		self.__newsApp.show( super( ).x( ), super( ).y( ))


	def readNews( self ):
		self.setEnabled( False )
		self.__readApp.fillTable( self.__newsStoryFile )
		self.__readApp.show( super( ).x( ), super( ).y( ))

	def enableWindow( self ):
		self.setEnabled( True )

	def updateNews( self ):
		self.enableWindow( )
		self.__newsList.updateTables( self.__sourcesFile, self.__categoryFile )
		self.__newsList.updateCountry( self.__countryFile )
		self.sendToServer( self.__newsStoryFile )

	def closeEvent( self, event ):
		self.__run_threads = False

	def sendToServer( self, file ):
		try:
			thread = threading.Thread( target=self.__socketClient.sendToServer, args =( file, 0.1 ))
			thread.start( )

		except:
			print( "Unable to send file <", file, ">" )
