#monthToRender=0 -> CurrentMonth
from source.app.modules.clockDate import clockDate
from source.app.drawPygame import drawPygame
from source.extra.fileIO import fileIO
import pygame
import time

class mycalendar(drawPygame):
	__rectPos = 0 
	__fileIO = fileIO( )

	def __init__( self, xOffset, yOffset, move ):
		super( ).__init__( xOffset, yOffset, move )

		self.__text = []
		self.__month = []
		self.__eventCount = []
		self.__count = []
		self.__renderFlag = True

	def renderText( self, color, font, dateToRender):
		date = clockDate( )
		if( dateToRender == 0 ):
			mnt = date.getCurMonth( )
		else:
			mnt = date.getNthMonth( dateToRender )

		self.__month = date.formatForPygame( mnt )
		self.__text = [ ]

		for i, m in enumerate( self.__month ):
			self.__text.append( font.render( m, True, color ))
			try:
				m = int( m )
			except:
				continue
			if( m == int( date.getDate( ).split( "." )[0])):
				self.__rectPos = i

	def renderEventCount( self, color, font, file):
		while( not self.__renderFlag ):
			time.sleep( 0.001 )
		self.__renderFlag = False
		self.__eventCount = []
		self.__count = []
		for i in range( len( self.__month )):
			fileToOpen = file + self.__month[i].strip( ) + ".txt"

			self.__count.append( self.__fileIO.getNumOfLines( fileToOpen ))
			self.__eventCount.append( font.render( str( self.__count[i] ), True, color ))

	def drawText( self, screen, colorInv ):
		if( super( ).getDrawFlag( )):
			j = 0
			z = 0
			while( len( self.__text ) > len( self.__count )):
				print( len( self.__text ), " <> ", len( self.__count ))
				time.sleep( 0.001)
			for i in range( len( self.__text )):
				if( not i % 7 and i != 0 ):
					j += 1
					z = 0
				screen.blit(self.__text[i], ( super( ).getStep( )*super( ).getXoffset( ) + z*( super( ).getStep( ) - super( ).getMove( )), 
										      super( ).getStep( )*super( ).getYoffset( ) + j*( super( ).getStep( ) - super( ).getMove( ))))
				
				try:
					if( j > 0 and self.__month[i] != "" and self.__count[i] > 0 ):
						screen.blit(self.__eventCount[i], ( ( super( ).getStep( )*super( ).getXoffset( )+ z*( super( ).getStep( ) - super( ).getMove( ) ) ) + super( ).getStep( ) - super( ).getMove( ) -22, 
										      			( super( ).getStep( )*super( ).getYoffset( ) + j*( super( ).getStep( ) - super( ).getMove( ) ) + super( ).getStep( ) - super( ).getMove( ) -18)))
				except:
					print("self.__month[i] = ", len( self.__month), "\nself.__count[i] = ", len(self.__count), "\nself.__text = ", len(self.__text))					
				if( i == self.__rectPos ):
					pygame.draw.rect( screen, colorInv, pygame.Rect( super( ).getStep( )*super( ).getXoffset( )-4 + z*( super( ).getStep( ) - super( ).getMove( )), 
																	 super( ).getStep( )*super( ).getYoffset( ) + j*( super( ).getStep( ) - super( ).getMove( )), 
																	 super( ).getStep( ) - super( ).getMove( ), super( ).getStep( ) - super( ).getMove( )), 1 )

				z += 1
			self.__renderFlag = True