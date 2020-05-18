import os
from pathlib import Path

class initFoldersAndFiles:
	folderNames = [ "data", "data/configFiles", "data/events", "data/news", "data/weather" ]
	files = [{ 'Name' : "data/configFiles/brightnessFile.txt", 'Value' : "100" }, 
			 { 'Name' : "data/configFiles/colorFile.txt", 'Value' : "#00ffff:#ff0000" }, 
			 { 'Name' : "data/news/countryFile.txt", 'Value' : "Serbia;~sepa~;rs" }, 
			 { 'Name' : "data/configFiles/fontFile.txt", 'Value' : "Times\n12" }, 
			 { 'Name' : "data/weather/weather.txt", 'Value' : "Celsius\nNovi Sad" },
			 { 'Name' : "data/news/categoryFile.txt", 'Value' : "General"},
			 { 'Name' : "data/configFiles/speedFile.txt", 'Value' : "5"},
			 { 'Name' : "data/configFiles/viewFile.txt", 'Value' : "Default"}]

	def initAllFiles( self ):
		for f in self.files:
			if( not Path( f[ 'Name' ]).exists( )):
				file = open( f[ 'Name' ], "w")
				file.write( f['Value'])
				file.close( )

	def initAllFolders( self ):
		for f in self.folderNames:
			if( not Path( f ).exists( )):
				os.mkdir( f )
