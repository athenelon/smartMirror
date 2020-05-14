from source.newsApp.story import story
from source.extra.fileIO import fileIO
from newsapi import NewsApiClient
import requests
import random

class newsApiHandler:
	__apiKey = '4135e2a067ea41d19f8013a073ffc10f'
	__story = []
	__countryID = ''
	__progressBar = None
	
	def __init__( self, progressBar ):
		self.__newsapi = NewsApiClient( api_key=self.__apiKey )
		self.__fileIO = fileIO( )
		self.__progressBar = progressBar

	def setCountryID( self, ID ):
		self.__countryID = ID

	def pullCategory( self, categoryList ):
		progressValue = 0
		self.__progressBar.show( )
		for category in categoryList:
			progressValue += 100 / len( categoryList )
			self.__progressBar.setValue( progressValue )
			if( self.__countryID in 'ww' ):
				news = self.__newsapi.get_top_headlines( category=category.lower( ),
														 language="en" )
			else:
				news = self.__newsapi.get_top_headlines( category=category.lower( ),
												   country=self.__countryID )
			self.fillStory( news )
		self.__progressBar.hide( )
		self.__progressBar.setValue( 0 )

	def pullSource( self, sourceList ):
		news = self.__newsapi.get_everything( sources=','.join( sourceList ))
		self.fillStory( news )

	def pullSourceNames( self ):
		if( self.__countryID in "ww" ):
			ID = 'ww'
		else:
			ID = "country=" + self.__countryID

		url = 'http://newsapi.org/v2/sources?' + ID + '&apiKey=' + self.__apiKey
		return ( requests.get( url ).json( ))['sources']

	def fillStory( self, news ):
		articles = news['articles']
		for singeleStory in articles:
			self.__story.append( story( singeleStory['url'], singeleStory['title'] ))

	def writeToFile( self, file ):
		for story in self.__story:
			story.writeToFile( file )

	def shuffleStory( self ):
		random.shuffle( self.__story )

	def newNewsRequest( self, file ):
		self.__story = []
		self.__fileIO.clearFile( file )