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
	__prevView = ''

	__scrollUpdateFlag = True
#------------------------------calendar------news--------events-------weather----------
	__defaultOffset       = [(6.5, 0, 10), (.5, 6, 32),(.5, 1.2, 32),(13, 0, 12)]
	__defaultOffsetPlus   = [(6.5, 0, 10), (.5, 6, 32),(.5, 1.2, 32),(13, 0, 12)]
	__calendarPlusEvents  = [(6.5, 0, -20),(0, 0, 0),  (.5, 1.2, 32),(0, 0, 0)]
	__calendarPlusWeather = [(6.5, 0, -20),(0, 0, 0),  (0, 0, 0),    (.25, 1.2, 12)]
	__calendarPlusWPlusE  = [(6.5, 0, -20),(0, 0, 0),  (.5, 1.2, 32),(.25, 6, 12)]
	__calendarPlusWPlusEP = [(6.5, 0, -8), (0, 0, 0),  (.5, 1.2, 32),(0, 7.9, 20)]
#-----------------------------calendar-------news--------events-------weather----------
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
		pygame.display.set_caption( "Smart Mirror" )
		pygame.time.set_timer( pygame.USEREVENT + 1, 5000 )

		self.__config.setColor( )
		self.__config.setBrightness( )
		self.__fonts = self.__config.getAllFonts( )

		self.__clock = pygame.time.Clock( )
		#self.__screen = pygame.display.set_mode((1024, 600),pygame.FULLSCREEN)
		self.__screen = pygame.display.set_mode((1024, 600))

		self.__run = True

		self.__newsIndex = 0
		self.__eventsIndex = 0

		self.addJobs( )

	def addJobs( self ):
		self.__scheduler = BackgroundScheduler( )
		self.__scheduler.add_job( self.__weather.getWeather, "interval", hours=3 )#warning:not rendering
		self.__scheduler.add_job( lambda: self.__socketServer.setWeatherFlag( True ), "interval", hours=3, minutes=1 )
		self.__scheduler.add_job( self.__news.getNews, "interval", hours=3 )#warning:not rendering
		self.__scheduler.add_job( lambda: self.__socketServer.setNewsFlag( True ), "interval", hours=3, minutes=1 )
		self.__scheduler.add_job( self.renderDate, "cron", hour=0 )
		self.__scheduler.add_job( self.renderTime, "cron", second=0 )

		self.__scheduler.start( )

	def renderDate( self ):
		print( "RENDERING DATE AUTOMATED")
		day, mnt, year = self.__time.getDate( ).split( " " )
		if( day[0] == '0' ):
			day = day[1:3]
		self.__eventsFile = "data/events/" + year[:-1] + "/" + mnt + "/" + day + "txt"
		
		self.__calendar.renderText( self.__color, self.__fonts[0], 0 )
		self.__calendar.renderEventCount( self.__colorInv, self.__fonts[7], "data/events/" + year[:-1] + "/" + mnt + "/" )
		self.__time.renderDate( self.__color, self.__fonts[1] )
		self.__time.renderWeekDay( self.__color, self.__fonts[1] )

	def renderNews( self ):
		if( self.__socketServer.getNewsFlag( )):
			self.__socketServer.setNewsFlag( False )
			self.__news.getNewsFromFile( )
			self.__news.renderText( self.__color, self.__fonts[4], self.__news.getText( ), self.__step * self.__newsWidth )#self.__step*10.3 )

	def renderWeather( self ):
		if( self.__socketServer.getWeatherFlag( )):
			self.__socketServer.setWeatherFlag( False )
			self.__weather.renderText( self.__color, self.__colorInv, self.__fonts[6], self.__fonts[5] )

	def getWeather( self ):
		if( self.__socketServer.getWeatherGetFlag( )):
			self.__socketServer.setWeatherGetFlag( False )
			self.__weather.getWeather( )

	def renderTime( self ):
		self.__time.renderTime( self.__color, self.__fonts[2] )

	def renderEvents( self ):
		if( self.__socketServer.getEventFlag( )):
			self.__socketServer.setEventFlag( False )
			self.renderDate( )
			text = self.__fileIO.simpleRead( self.__eventsFile, multiLine=True )
			if( text == [] or text == '' ):
				text = [ "Nothing to do today..." ]
			self.__events.renderText( self.__colorInv, self.__fonts[3], text, self.__step*4.8 )
			

	def setParam( self, xS, yS, xE, yE, nN, eN, nW, now, enh, nC ):
		self.__xS = xS
		self.__yS = yS
		self.__xE = xE
		self.__yE = yE
		self.__newsNum = nN
		self.__eventsNum = eN
		self.__newsWidth = nW
		self.__numOfWeather = now
		self.__everyNumOfHours = enh
		self.__numOfColumn = nC

	def setOffset( self, view ):
		if( view != self.__prevView ):
			if( view == "Default" ):
				self.setParam( .5, 5.8, 6, 5.8, 7, 9, 10.3, 12, 2, 1 )
				self.__config.setCSize( 0 )
				self.__calendar.setOffset( self.__defaultOffset[0])
				self.__news.setOffset( self.__defaultOffset[1])
				self.__events.setOffset( self.__defaultOffset[2])
				self.__weather.setOffset( self.__defaultOffset[3])
			elif( view == "Default+" ):
				self.setParam( .5, 5.8, 6, 5.8, 7, 9, 14, 8, 2, 1 )
				self.__config.setCSize( 0 )
				self.__calendar.setOffset( self.__defaultOffsetPlus[0])
				self.__news.setOffset( self.__defaultOffsetPlus[1])
				self.__events.setOffset( self.__defaultOffsetPlus[2])
				self.__weather.setOffset( self.__defaultOffsetPlus[3])
			elif( view == "Calendar+Events" ):
				self.setParam( .5, 9.2, 6, 9.2, 0, 16, 0, 0, 0, 0)
				self.__config.setCSize( 16 )
				self.__calendar.setOffset( self.__calendarPlusEvents[0])
				self.__news.setOffset( self.__calendarPlusEvents[1])
				self.__events.setOffset( self.__calendarPlusEvents[2])
				self.__weather.setOffset( self.__calendarPlusEvents[3])
			elif( view == "Calendar+Weather" ):
				self.setParam( .5, 9.2, 6, 9.2, 0, 16, 0, 10, 1, 2 )
				self.__config.setCSize( 16 )
				self.__calendar.setOffset( self.__calendarPlusWeather[0])
				self.__news.setOffset( self.__calendarPlusWeather[1])
				self.__events.setOffset( self.__calendarPlusWeather[2])
				self.__weather.setOffset( self.__calendarPlusWeather[3])
			elif( view == "Calendar+Weather+Events" ):
				self.setParam( .5, 5.8, 6, 5.8, 0, 9, 0, 8, 2, 2 )
				self.__config.setCSize( 16 )
				self.__calendar.setOffset( self.__calendarPlusWPlusE[0])
				self.__news.setOffset( self.__calendarPlusWPlusE[1])
				self.__events.setOffset( self.__calendarPlusWPlusE[2])
				self.__weather.setOffset( self.__calendarPlusWPlusE[3])
			elif( view == "Calendar+Weather+Events+" ):
				self.setParam( .5, 7.7, 6, 7.7, 0, 13, 0, 12, 2, 6 )
				self.__config.setCSize( 12 )
				self.__calendar.setOffset( self.__calendarPlusWPlusEP[0])
				self.__news.setOffset( self.__calendarPlusWPlusEP[1])
				self.__events.setOffset( self.__calendarPlusWPlusEP[2])
				self.__weather.setOffset( self.__calendarPlusWPlusEP[3])
			
	def draw( self ):	
		self.__time.drawTime( self.__screen )
		self.__time.drawDate( self.__screen )
		self.__time.drawWeekDay( self.__screen )

		self.__calendar.drawText( self.__screen, self.__colorInv )
		self.__weather.drawText( self.__screen, self.__numOfWeather, self.__everyNumOfHours, self.__numOfColumn )
		self.__newsIndex = self.__news.drawText( self.__screen, self.__newsIndex, self.__newsNum )
		self.__eventsIndex = self.__events.drawText( self.__screen, self.__eventsIndex, self.__eventsNum )

	def drawConstant( self ):
		pygame.draw.line( self.__screen, self.__color, (self.__step*.5, self.__step*1.1), (self.__step*6 -5, self.__step*1.1), 1 )
		pygame.draw.line( self.__screen, self.__color, (self.__step*self.__xS, self.__step*self.__yS), (self.__step*self.__xE -5, self.__step*self.__yE), 1 )
	
	def setConfig( self ):
		if( self.__socketServer.getConfigFlag( )):
			self.__socketServer.setConfigFlag( False )
			self.__socketServer.setEventFlag( True )
			self.__socketServer.setNewsFlag( True )
			self.__socketServer.setWeatherFlag( True )

			view = self.__config.getView( )
			self.setOffset( view )
			self.__prevView = view

			self.__fonts = self.__config.getAllFonts( )
			self.__color, self.__colorInv = self.__config.setColor( )
			self.__config.setBrightness( )
			self.__config.setSleepTime( )

			self.renderTime( )
			
			pygame.time.set_timer( pygame.USEREVENT + 1, self.__config.getSpeed( ))
			
	def runMirror( self ):
		self.__socketServer.setConfigFlag( True )
		self.__weather.getWeather( )
		self.__news.getNews( )

		while( self.__run ):
			self.setConfig( )
			self.getWeather( )
			self.renderNews( )
			self.renderEvents( )
			self.renderWeather( )
			self.drawConstant( )
			self.draw( )

			for event in pygame.event.get( ):
				if( event.type == pygame.QUIT ):
					self.__run = False
					self.__socketServer.stopServer( )
				if ( event.type == pygame.KEYDOWN ):
					if( event.key == pygame.K_ESCAPE ):
						self.__screen = pygame.display.set_mode((1024, 600), 0)
						pygame.mouse.set_visible( True )
					elif( event.key == pygame.K_f ):
						self.__screen = pygame.display.set_mode((1024, 600), pygame.FULLSCREEN)
						pygame.mouse.set_visible( False )
				if( event.type == pygame.USEREVENT+1 ):
					self.__newsIndex += 1
					self.__eventsIndex += 1

			pygame.display.update( )
			self.__screen.fill( self.__blackAsNight )

			self.__clock.tick( 30 )