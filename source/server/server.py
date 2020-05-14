import socket
import time
import threading
from source.extra.fileIO import fileIO

class socketServer:
	ip = '127.0.0.1'
	port = 8080

	def __init__( self ):
		
		self.__listenFlag = True
		self.__runFlag = True 

		self.__eventFlag = False
		self.__configFlag = False
		self.__weatherFlag = False
		self.__newsFlag = False
		self.__weatherGetFlag = False

		self.__fileIO = fileIO( )

		self.__server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.__server.bind(( self.ip, self.port ))
		self.__server.listen( 5 )

		delay = 0.1
		listenThread = threading.Thread( target=self.listenForClient, args=(delay,))
		listenThread.start( )

	def getEventFlag( self ):
		return self.__eventFlag
	def getConfigFlag( self ):
		return self.__configFlag
	def getWeatherFlag( self ):
		return self.__weatherFlag
	def getNewsFlag( self ):
		return self.__newsFlag
	def getWeatherGetFlag( self ):
		return self.__weatherGetFlag

	def setEventFlag( self, state ):
		self.__eventFlag = state
	def setConfigFlag( self, state ):
		self.__configFlag = state
	def setWeatherFlag( self, state ):
		self.__weatherFlag = state
	def setNewsFlag( self, state ):
		self.__newsFlag	 = state
	def setWeatherGetFlag( self, state ):
		self.__weatherGetFlag = state

	def listenForClient( self, delay ):
		while( self.__listenFlag ):
			print( "Server is listening...")
			conn, addr = self.__server.accept( )
			print( "\n\nClient <" + str(addr[ 1 ]) + "> Connected...")
			thread = threading.Thread( target=self.clientThread, args=(conn, addr, delay))
			thread.start( )

	def clientThread( self, conn, addr, delay ):
		runFlag = True
		while( runFlag ):
			data, runFlag = self.getClientData( conn, runFlag )
			runFlag = self.setClientData( data, runFlag )
			
		print( "\nClient <" + str( addr[ 1 ]) + "> Disconnected...\n")
		time.sleep( delay )
		conn.close( )

	def getClientData( self, conn, runFlag ):#use decode when u have everything
		data = b''
		dataSegment = conn.recv( 4096 )

		while( len( dataSegment ) >= 1 ):
			if( b"clientPing" in dataSegment ):
				print( "\033[92m clientPing \033[0m" )
				break

			if( b"~pingDisc~" in dataSegment ):
				print( "Disconnecting ping thread")
				runFlag = False
				break
			
			data += dataSegment
			dataSegment = conn.recv( 4096 )
		return data.decode( ), runFlag

	def setClientData( self, data, runFlag ):
		if( len( data ) >= 1 ):
			data = data.split( ";~;" )
			if( "~file~" in data[ 0 ]):
				print( "\033[91m" + data[ 1 ] + "\033[0m" )
				self.__fileIO.makePath( data[ 1 ])

			if( "~data~" in data[ 2 ] ):
				self.__fileIO.simpleWrite( data[ 1 ], data[ 3 ], newLine=True )
				self.updateFlags( data[1] )

			if( "~disc~" in data ):
				runFlag = False
				print( "disc")
		return runFlag

	def updateFlags( self, data ):
		if( "data/events" in data ):
			self.__eventFlag = True
		if( "data/configFiles" in data ):
			self.__configFlag = True
		if( "data/weather" in data ):
			self.__weatherFlag = True
			self.__weatherGetFlag = True
		if( "data/news" in data ):
			self.__newsFlag = True

	def stopServer( self ):
		self.__runFlag = False
		self.__listenFlag = False
		self.__server.close( )