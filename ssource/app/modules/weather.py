from source.extra.fileIO import fileIO
import requests
import pygame

class weather:
	__apiKey = "axtloV8pqzpCuvRImrZgGhASPTbDSphV"
	__step = 64
	__iconPath = "data/weather/icons/"
	__weatherFile = "data/weather/weather.txt"

	__fileIO = fileIO( )

	def __init__( self, xOffset, yOffset, move ):
		pygame.init( )
		self.__weather = []
		self.__data = []
		self.__xOffset = xOffset * self.__step
		self.__yOffset = yOffset * self.__step
		self.__move = move
		self.__metric = "True"

	def saveWeatherFormat( self, weather ):
		self.__data = []
		for hour in weather:
			hourlyData = hour[ 'DateTime' ].split( "T" )[1] + "~" + str( hour[ 'WeatherIcon' ]) + "~" + str( hour[ 'PrecipitationProbability']) + "~" + str( hour[ 'Temperature'][ 'Value' ])
			self.__data.append( hourlyData )

	def getWeather( self ):
		weatherConfig = self.__fileIO.simpleRead( self.__weatherFile, multiLine=True )
		if( weatherConfig[0] in "Celsius"):
			self.__metric = "True"
		else:
			metric = "False"
		city = weatherConfig[1]

		url = "http://dataservice.accuweather.com/locations/v1/cities/RS/search?apikey= " + self.__apiKey + "&q=" + city
		result = requests.get( url ).json( )
		url = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/" + result[ 0 ][ 'Key' ] + "?apikey= " + self.__apiKey + "&metric=" + self.__metric
		weather = requests.get( url ).json( )

		self.saveWeatherFormat( weather )

	def renderText( self, color, colorInv, hFont, font ):
		self.__hour = []
		self.__icon = []
		self.__perc = []
		self.__temp = []
		for t in self.__data:
			hour, icon, perc, temp = t.split( "~" )
			self.__hour.append( hFont.render( hour.split( ":" )[0] + ":" + hour.split( ":" )[1], True, colorInv ))
			self.__perc.append( font.render( perc + "%", True, color ))
			if( self.__metric ):
				self.__temp.append( font.render( str(round(float(temp))) + '\u2103', True, color ))# *C
			else:
				self.__temp.append( font.render( str(round(float(temp))) + '\u2109', True, color ))# *F

			self.icon.append( pygame.image.load( self.iconPath + icon + ".png" ))
		
	def drawText( self, screen ):
		for i in range( 0, len(self.__hour), 2 ):
			screen.blit( self.__hour[i], ( self.__xOffset + self.__step*1.9, self.__yOffset + i*(self.__step-self.__move )))
			screen.blit( self.__perc[i], ( self.__xOffset + self.__step*.5, self.__yOffset + self.__step*.66 + i*( self.__step-self.__move )))
			screen.blit( self.__temp[i], ( self.__xOffset + self.__step*.5, self.__yOffset + i*(self.__step-self.__move )))
			screen.blit( self.__icon[i], ( self.__xOffset + self.__step*1.7, self.__yOffset + self.__step*.5 + i*(self.__step-self.__move )))
			pygame.draw.line( screen, (0,255,255), (self.__xOffset + self.__step*.5, self.__yOffset + self.__step * 1.2 + i*(self.__step-self.__move )),
												   (self.__xOffset + self.__step*1.25, self.__yOffset + self.__step * 1.2 + i*(self.__step-self.__move )), 1 )