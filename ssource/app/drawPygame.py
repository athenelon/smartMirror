from source.extra.fileIO import fileIO

class drawPygame:
	__step = 64
	def __init__( self, xOffset, yOffset, move ):
		self.__xOffset = xOffset
		self.__yOffset = yOffset
		self.__move = move
		self.__fileIO = fileIO( )

		self.__text = []

	def renderText( self, color, font, text, maxWidthForWrap, maxLinesPerWrap=2 ):
		self.__text = []

		for i, textSeg in enumerate( text ):
			if( len( textSeg ) > 1 ):
				for line in self.wrapText( font, textSeg, maxWidthForWrap, maxLinesPerWrap ):
					self.__text.append( font.render( line, True, color ))

					#if( maxHeightInLines <= len( self.__text )):
					#	return len( self.__text )

	def drawText( self, screen, index, maxHeightInLines ):
		if( index >= len( self.__text ) - maxHeightInLines +1 ):
			print( "len text", len( self.__text ))
			index = 0
		for i in range( index, index + maxHeightInLines ):
			screen.blit( self.__text[i], ( self.__step*self.__xOffset, 
										   self.__step*self.__yOffset + (i-index)*(self.__step-self.__move )))
		print("tick")
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