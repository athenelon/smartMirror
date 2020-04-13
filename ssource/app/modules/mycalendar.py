#monthToRender=0 -> CurrentMonth
from source.app.modules.clockDate import clockDate
from source.app.drawPygame import drawPygame
import pygame

class mycalendar(drawPygame):
	__rectPos = 0 
	__step = 64
	def __init__( self, xOffset, yOffset, move ):
		super( ).__init__( xOffset, yOffset, move )
		self.__xOffset = xOffset
		self.__yOffset = yOffset
		self.__move = move

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

	def drawText( self, screen, colorInv ):
		j = 0
		z = 0
		for i in range( len(self.__text )):
			if( not i % 7 and i != 0 ):
				j += 1
				z = 0
			screen.blit(self.__text[i], ( self.__step*self.__xOffset + z*( self.__step - self.__move ), 
									      self.__step*self.__yOffset + j*( self.__step - self.__move )))

			if( i == self.__rectPos ):
				pygame.draw.rect( screen, colorInv, pygame.Rect( self.__step*self.__xOffset + z*( self.__step - self.__move  ), 
																 self.__step*self.__yOffset + j*( self.__step - self.__move  ), 
																 self.__step*.8, self.__step*.8 ), 1 )

			z += 1