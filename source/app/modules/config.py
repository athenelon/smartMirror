from source.extra.fileIO import fileIO
import sys
import pygame

class config:
	__white = (255, 255, 255)
	__red = (255, 0, 0)
	__color = ( 0, 255, 255 )
	__colorInv = __red
	__colorFile = "data/configFiles/colorFile.txt"
	__brightnessFile = "data/configFiles/brightnessFile.txt"
	__fontFile = "data/configFiles/fontFile.txt"
	__speedFile = "data/configFiles/speedFile.txt"
	__viewFile = "data/configFiles/viewFile.txt"

	__fileIO = fileIO( )

	def __init__( self ):
		self.__fonts = [0] *8
		self.__cSize = 0

	def setColor( self ):
		color, colorInv = self.__fileIO.simpleRead( self.__colorFile, separator=":" )
		self.__color = [int( color[ i : i +2 ], 16 ) for i in range( 1, len(color) -1, 2 )]
		self.__colorInv = [int( colorInv[ i : i +2 ], 16 ) for i in range( 1, len(colorInv) -1, 2 )]
		if( self.__color == self.__white ): 
			self.__colorInv = self.__red

		return self.__color, self.__colorInv

	def setBrightness( self ):
		brightness = self.__fileIO.simpleRead( self.__brightnessFile )
		if( sys.platform == "linux" or sys.platform == "linux2" ):
			import os
			os.system( 'xbacklight -set ' + brightness )
		elif( sys.platform == "win32" ):
			import wmi
			wmi.WMI( namespace='wmi' ).WmiMonitorBrightnessMethods( )[0].WmiSetBrightness( int( brightness ), 1 )

	def readFontFromFile( self ):
		font = self.__fileIO.simpleRead( self.__fontFile, multiLine=True )
		font[ 0 ] = font[ 0 ].split( "," )[ 0 ]
		font[ 1 ] = int( font[ 1 ])
		if( len( font ) == 2 ):
			font.append( False )
			font.append( False )
		elif( len( font ) == 3 ):
			if( 'Bold' in font[ 2 ]):
				font[ 2 ] = True
				font.append( False )
			else:
				font[ 2 ] = False
				font.append( True )
		elif( len( font ) == 4 ):
			font[ 2 ] = True
			font[ 3 ] = True
		return font

	def getFont( self, index ):
		return self.__fonts[index]
	def setCSize( self, size ):
		self.__cSize = size

	def getSpeed( self ):
		speed = self.__fileIO.simpleRead( self.__speedFile )
		if( "Non" in speed ):
			return 0
		else:
			return int( speed ) *1000

	def getView( self ):
		return self.__fileIO.simpleRead( self.__viewFile, multiLine=True )[0]

	def getAllFonts( self ):
		fontName, fontSize, bold, italic = self.readFontFromFile( )
		try:		
			self.__fonts[0] = pygame.font.SysFont( fontName, fontSize + self.__cSize, bold=bold, italic=italic )#calendar
			self.__fonts[1] = pygame.font.SysFont( fontName, fontSize + 0 , bold=bold, italic=italic )#date
			self.__fonts[2] = pygame.font.SysFont( fontName, fontSize + 32 , bold=bold, italic=italic )#time
			self.__fonts[3] = pygame.font.SysFont( fontName, fontSize -12 , bold=bold, italic=italic )#events
			self.__fonts[4] = pygame.font.SysFont( fontName, fontSize - 12 , bold=bold, italic=italic )#news
			self.__fonts[5] = pygame.font.SysFont( fontName, fontSize - 4, bold=bold, italic=italic )#weather
			self.__fonts[6] = pygame.font.SysFont( fontName, fontSize - 12 , bold=bold, italic=italic )#hour
			self.__fonts[7] = pygame.font.SysFont( fontName, fontSize - 18 , bold=bold, italic=italic )#hour
		except:
			self.__fonts[0] = pygame.font.Font( fontName, fontSize , bold=bold, italic=italic )
			self.__fonts[1] = pygame.font.Font( fontName, fontSize + 0 , bold=bold, italic=italic )
			self.__fonts[2] = pygame.font.Font( fontName, fontSize + 32 , bold=bold, italic=italic )
			self.__fonts[3] = pygame.font.Font( fontName, fontSize -12 , bold=bold, italic=italic )
			self.__fonts[4] = pygame.font.Font( fontName, fontSize - 12 , bold=bold, italic=italic )
			self.__fonts[5] = pygame.font.Font( fontName, fontSize - 4 , bold=bold, italic=italic )
			self.__fonts[6] = pygame.font.Font( fontName, fontSize - 12 , bold=bold, italic=italic )
			self.__fonts[7] = pygame.font.Font( fontName, fontSize - 18 , bold=bold, italic=italic )
		return self.__fonts