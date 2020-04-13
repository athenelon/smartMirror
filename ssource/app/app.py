import os
os.environ['SDL_AUDIODRIVER'] = 'dsp' #ALSA uses 100%+ CPU time, dsp does not

import pygame
from apscheduler.schedulers.background import BackgroundScheduler

from source.app.modules.clockDate import clockDate
from source.app.modules.mycalendar import mycalendar
from source.app.modules.news import news
from source.app.modules.events import events
from source.app.modules.weather import weather
from source.app.modules.config import config

from source.extra.initFoldersAndFiles import initFoldersAndFiles
from source.extra.fileIO import fileIO
from source.server.server import socketServer

class app:
	__blackAsNight = (0, 0, 0)
	__color = ( 0, 255, 255 )
	__colorInv = ( 255,0, 0 )

	__fontName = "Times New Roman"
	__fontSize = 32
	__bold = False
	__italic = False

	__eventsFile = "data/events/"

	__step = 64

	__scrollUpdateFlag = True

	def __init__( self ):
		self.__time = clockDate( )
		self.__calendar = mycalendar( 6.5, 0, 10 )
		self.__news = news( .5, 6, 32 )
		self.__events = events( .5, 1.2, 32 )
		self.__weather = weather( 13, 0, 12 )
		self.__config = config( )
		self.__fileIO = fileIO( )
		self.__socketServer = socketServer( )
		self.__initFoldersAndFiles = initFoldersAndFiles( )

		self.__initFoldersAndFiles.initAllFolders( )
		self.__initFoldersAndFiles.initAllFiles( )

		pygame.init( )
		pygame.time.set_timer( pygame.USEREVENT + 1, 5000 )

		self.__config.setColor( )
		self.__config.setBrightness( )
		self.__fonts = self.__config.getAllFonts( )



		self.__clock = pygame.time.Clock( )
		self.__screen = pygame.display.set_mode((1024, 600))
		self.__run = True

		self.__newsIndex = 0
		self.__eventsIndex = 0

		self.addJobs( )

	def addJobs( self ):
		self.__scheduler = BackgroundScheduler( )
		self.__scheduler.add_job( self.__weather.getWeather, "interval", hours=3 )#warning:not rendering
		self.__scheduler.add_job( self.__news.getNews, "interval", hours=3 )
		self.__scheduler.add_job( self.renderDate, "cron", hour=0 )
		self.__scheduler.add_job( self.renderTime, "cron", hour=0 )

		self.__scheduler.start( )

	def renderDate( self ):
		day, mnt, year = self.__time.getDate( ).split( " " )
		if( day[0] == '0' ):
			day = day[1:3]
		self.__eventsFile = "data/events/" + year[:-1] + "/" + mnt + "/" + day + "txt"		
		
		self.__calendar.renderText( self.__color, self.__fonts[0], 0 )
		self.__time.renderDate( self.__color, self.__fonts[1] )
		self.__time.renderWeekDay( self.__color, self.__fonts[1] )

	def renderNews( self ):
		if( self.__socketServer.getNewsFlag( )):
			self.__socketServer.setNewsFlag( False )
			self.__news.getNewsFromFile( )
			self.__news.renderText( self.__color, self.__fonts[4], self.__news.getText( ), self.__step*10.3 )
			print( len ( self.__news.getText( )))

	def renderWeather( self ):
		if( self.__socketServer.getWeatherFlag( )):
			self.__socketServer.setWeatherFlag( False )
			self.__weather.renderText( self.__color, self.__colorInv, self.__fonts[6], self.__fonts[5] )

	def renderTime( self ):
		self.__time.renderTime( self.__color, self.__fonts[2] )

	def renderEvents( self ):
		if( self.__socketServer.getEventFlag( )):
			self.__socketServer.setEventFlag( False )
			text = self.__fileIO.simpleRead( self.__eventsFile, multiLine=True )

			if( text == [] ):
				text = [ "Nothing to do today..." ]
			self.__events.renderText( self.__colorInv, self.__fonts[3], text, self.__step*4.8 )

	def draw( self ):
		self.__weather.drawText( self.__screen )
		self.__calendar.drawText( self.__screen, self.__colorInv )

		self.__time.drawTime( self.__screen )
		self.__time.drawDate( self.__screen )
		self.__time.drawWeekDay( self.__screen )

		self.__newsIndex = self.__news.drawText( self.__screen, self.__newsIndex, 7 )
		self.__eventsIndex = self.__events.drawText( self.__screen, self.__eventsIndex, 9 )

	def drawConstant( self ):
		pygame.draw.line( self.__screen, self.__color, (self.__step*.5, self.__step*1.1), (self.__step*6 -5, self.__step*1.1), 1 )
		pygame.draw.line( self.__screen, self.__color, (self.__step*.5, self.__step*5.9), (self.__step*6 -5, self.__step*5.9), 1 )

	def setConfig( self ):
		if( self.__socketServer.getConfigFlag( )):
			self.__socketServer.setConfigFlag( False )
			self.__socketServer.setEventFlag( True )
			self.__socketServer.setNewsFlag( True )
			self.__socketServer.setWeatherFlag( True )

			self.__fonts = self.__config.getAllFonts( )
			self.__color, self.__colorInv = self.__config.setColor( )
			self.__config.setBrightness( )

			self.renderDate( )
			self.renderWeather( )
			self.renderNews( )
			self.renderTime( )
			
	def runMirror( self ):
		self.__socketServer.setConfigFlag( True )
		self.__socketServer.setEventFlag( True )
		self.__socketServer.setNewsFlag( True )
		self.__socketServer.setWeatherFlag( True )
		#self.__weather.getWeather( )
		#self.__news.getNews( )
		
		self.setConfig( )
		self.renderDate( )

		self.renderWeather( )

		self.renderNews( )
		self.renderTime( )
		self.renderEvents( )

		while( self.__run ):
			self.setConfig( )
			self.renderNews( )
			self.renderEvents( )
			self.drawConstant( )
			self.draw( )

			for event in pygame.event.get( ):
				if( event.type == pygame.QUIT ):
					self.__run = False
					self.__socketServer.stopServer( )
				if( event.type == pygame.USEREVENT+1 ):
					self.__newsIndex += 1
					self.__eventsIndex += 1

			pygame.display.update( )
			self.__screen.fill( self.__blackAsNight )

			self.__clock.tick( 30 )