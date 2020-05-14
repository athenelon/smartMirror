from source.mainApp.event import event
from source.extra.fileIO import fileIO
from source.client.client import socketClient

from PyQt5.QtWidgets import QTableWidgetItem
import threading

class eventHandler:
	__fileIO = fileIO( )
	__events = []
	__eventCount = 0
	__separator = ";~sepa~;"
	__path = ''

	def __init__( self, table, hour, minute, add, remove, text, label ):
		self.__table = table
		self.__hour = hour
		self.__minute = minute
		self.__add = add
		self.__remove = remove
		self.__text = text
		self.__label = label
		self.__socketClient = socketClient( '127.0.0.1', 8080 )

		#Focus Line Edit
		self.__text.setFocus( )

		self.__add.clicked.connect( self.addClicked )
		self.__text.returnPressed.connect( self.__add.click ) #Enter
		
		self.__remove.clicked.connect( self.removeClicked )

	def getPath( self ):
		return self.__path

	def getHour( self ):
		return self.__hour.currentIndex( )

	def getMinute( self ):
		return self.__minute.value( )

	def getTableHour( self, i ):
		return int( self.__table.item( i, 0 ).text().split(":")[ 0 ])

	def getTableMinute( self, i ):
		return int( self.__table.item( i, 0 ).text().split(":")[ 1 ])

	def getText( self ):#egg here
		eventText = str( self.__text.text( ))
		self.__text.setText( "" )
		return eventText

	def getTextLen( self ):
		return len( str( self.__text.text( )))

	def setLabel( self, date ):
		self.__label.setText( date )

	def setPath( self, path ):
		self.__path = path
		if( self.__fileIO.fileExists( path )):
			self.readFromFile( )
		else:
			self.clearContents( )

	def clearContents( self ):
		for i in range( len( self.__events ), 0, -1 ):
			self.__table.removeRow( i-1 )
			del self.__events[i-1]

	def addEvent( self, i ):
		self.__table.insertRow( i )

		time, text = self.__events[i].formatForTable( )
		self.__table.setItem( i, 0, QTableWidgetItem( time ))
		self.__table.setItem( i, 1, QTableWidgetItem( text ))
		self.updateTableConfig( )

	def addClicked( self ):
		if( self.getTextLen( )):
			self.__events.append( event( self.getHour( ), self.getMinute( ), self.getText( )))
			index = self.sort( )
			self.addEvent( index )
			self.writeToFile( )

	def sort( self ):
		newTime = self.__events[-1].formatForTable( )[0]
		for i, e in enumerate( self.__events ):
			time = e.formatForTable( )[0]
			if( e.getTime( ) > newTime ):
				self.__events.insert( i, self.__events.pop( len( self.__events ) -1 ))
				return i
		return i

	def removeClicked( self ):
		if( len( self.__events ) > 0 ):
			curRow = self.__table.currentRow( )
			if(( curRow == -1 )):
				curRow = 0
			self.__table.removeRow( curRow )
			del self.__events[curRow]
			self.__fileIO.removeNthLine( self.__path, curRow )
			self.sendToServer( self.__path )

	def updateTableConfig( self ):
		self.__table.resizeRowsToContents( )
		self.__table.scrollToBottom( )

	def writeToFile( self ):#not used
		self.__fileIO.makePath( self.__path )
		self.__fileIO.clearFile( self.__path )

		for e in self.__events:
			e.writeToFile( self.__path )

		self.sendToServer( self.__path )

	def readFromFile( self ):
		self.__events.clear( )
		self.__table.setRowCount( 0 )#clear table
		events = self.__fileIO.simpleRead( self.__path, multiLine=True, separator=self.__separator )

		for e in events:
			hour, minute = e[0].split(":")
			self.__events.append( event( hour, minute, e[1] ))
			self.addEvent( len( self.__events ) -1 )

	def clearFile( self ):
		self.__fileIO.clearFile( self.__path )

	def sendToServer( self, file ):
		try:
			thread = threading.Thread( target=self.__socketClient.sendToServer, args =( file, 0.1 ))
			thread.start( )

		except:
			print( "Unable to send file <", file, ">" )