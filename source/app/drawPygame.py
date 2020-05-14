from source.extra.fileIO import fileIO

class drawPygame:
	__step = 64
	def __init__( self, xOffset=0, yOffset=0, move=0 ):
		self.__xOffset = xOffset
		self.__yOffset = yOffset
		self.__move = move
		self.__fileIO = fileIO( )

		self.__text = []
		self.__drawFlag = True

	def setX( self, xOffset ):
		self.__xOffset = xOffset
	def setY( self, yOffset ):
		self.__yOffset = yOffset
	def setMove( self, move ):
		self.__move = move

	def setOffset( self, offset ):
		self.__xOffset = offset[0]
		self.__yOffset = offset[1]
		self.__move = offset[2]
		if( self.__xOffset == 0 and self.__yOffset == 0 and self.__move == 0 ):
			self.__drawFlag = False
		else:
			self.__drawFlag = True

	def getDrawFlag( self ):
		return self.__drawFlag
	def getXoffset( self ):
		return self.__xOffset
	def getYoffset( self ):
		return self.__yOffset
	def getMove( self ):
		return self.__move
	def getStep( self ):
		return self.__step

	def renderText( self, color, font, text, maxWidthForWrap, maxLinesPerWrap=2 ):
		self.__text = []
		for i, textSeg in enumerate( text ):
			if( len( textSeg ) > 1 ):
				for line in self.wrapText( font, textSeg, maxWidthForWrap, maxLinesPerWrap ):
					self.__text.append( font.render( line, True, color ))

	def drawText( self, screen, index, maxHeightInLines ):
		if( self.__drawFlag ):
			if( index >= len( self.__text ) - maxHeightInLines +1 ):
				index = 0

			for i in range( index, index + maxHeightInLines ):
				if( i >= len( self.__text )):#nothing to do today
					break
				screen.blit( self.__text[i], ( self.__step*self.__xOffset, 
											   self.__step*self.__yOffset + (i-index)*(self.__step-self.__move )))
				
		return index

	def wrapText( self, font, text, maxWidth, maxLines=2 ):
		words = text.split( " " )
		lines = []
		nlPos = 0
		for l in range( maxLines ):
			line = []
			if( l == 0 ):
				line.append( '\u2023' )
			else:
				line.append( '  ' )
			for i in range( nlPos, len( words )):
				line.append( words[ i ] )
				wordW, wordH = font.size( ' '.join( line ))
				if( wordW > maxWidth ):
					nlPos = i +1
					break
			lines.append( ' '.join( line ))
			if( i >= len( words )-1):
				break
		return lines