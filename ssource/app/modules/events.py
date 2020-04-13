from source.app.drawPygame import drawPygame

class events(drawPygame):
	__separator = ";~sepa~;"

	def __init__( self, xOffset, yOffset, move ):
		super( ).__init__( xOffset, yOffset, move )

	def renderText( self, color, font, text, maxWidthForWrap, maxLinesPerWrap=2 ):
		for i in range( len( text )):
			if( self.__separator in text[i] ):
				event = text[i].split( self.__separator )
				event = event[0] + " - " + event[1]
				text[i] = event
		super( ).renderText( color, font, text, maxWidthForWrap, maxLinesPerWrap )