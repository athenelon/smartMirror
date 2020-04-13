import datetime
import calendar
from source.app.drawPygame import drawPygame
class clockDate():
	step = 64

	def getTime( self ):
		return datetime.datetime.now( ).strftime( "%H:%M")

	def getDate( self ):
		return datetime.datetime.now( ).strftime( "%d. %b %Y.")

	def getWeekDay( self ):
		return datetime.datetime.now( ).strftime( "%A" )

	def getCurMonth( self ):
		return calendar.TextCalendar( ).formatmonth( int( datetime.datetime.now( ).strftime( "%Y")), 
													 int( datetime.datetime.now( ).strftime( "%m")))

	def getNthMonth( self, month ):
		return calendar.TextCalendar( ).formatmonth( month )

	def formatForPygame( self, month ):
		month = month.splitlines( )
		data = []
		for i in range( 1, len( month )):
			for j in range( 0, len( month[ i ]) -1, 3 ):
				data.append( month[i][j] + month[i][j+1])
		return data

	def renderTime( self, color, font ):
		self.__time = font.render( self.getTime( ), True, color )

	def renderDate( self, color, font ):
		self.__date = font.render( self.getDate(), True, color )

	def renderWeekDay( self, color, font ):
		self.__weekDay = font.render( self.getWeekDay(), True, color )

	def drawTime( self, screen ):
		screen.blit( self.__time, ( self.step*.5, self.step*0 ))

	def drawDate( self, screen ):
		screen.blit( self.__date, ( self.step*3, self.step*.1 ))

	def drawWeekDay( self, screen ):
		screen.blit( self.__weekDay, ( self.step*3, self.step*.5 ))