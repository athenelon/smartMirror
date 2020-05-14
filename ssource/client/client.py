import socket
import threading
import time

class socketClient( ):
	def __init__( self, ip, port ):
		self.__ip = ip
		self.__port = port

	def connectToServer( self ):
		self.__client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		try:
			self.__client.connect(( self.__ip, self.__port ))
			return True
		except:
			print( "IN:client::connectToServer: unable to connect to server!" )
			return False
			
	def sendToServer( self, fileName, delay ):
		if( self.connectToServer( )):

			strToSend = "~file~;~;" + fileName + ";~;~data~;~;" + open( fileName, "r", encoding="utf-8" ).read( ) + ";~;~disc~;~;"
			self.__client.send( strToSend.encode( ))
			time.sleep( 0.01 )
			self.__client.close( )

	def checkIfConnected( self, delay, QtLabel, run ):
		flag = False

		while( run( )):
			try:
				pingClient = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
				pingClient.connect(( self.__ip, self.__port ))
				flag = True 
				print( "True in 1st While" )
			except:
				flag = False
				QtLabel.setText( "No Connection with Smart Mirror!" )
				QtLabel.setStyleSheet( "color:red")
				print( "False in 1st While" )
			if( flag ):
				while( run( )):
					try:
						pingClient.send( "clientPing".encode( ))
						QtLabel.setText( "Connected to Smart Mirror" )
						QtLabel.setStyleSheet( "color:green")
						print( "True in 2nd While" )
					except:
						print( "False in 2nd While" )
						QtLabel.setText( "No Connection with Smart Mirror!" )
						QtLabel.setStyleSheet( "color:red")
						break
					time.sleep( delay )
				try:
					pingClient.send( "~pingDisc~".encode( ))
				except:
					print( "Cant send pingDisc signal")
				finally:
					time.sleep( 0.1 )
					pingClient.close( )
				print( "Left 2nd While" )
			else:
				time.sleep( delay )
