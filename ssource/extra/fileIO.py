from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import fileinput
import os
#import filter

class fileIO:
	def simpleRead( self, fileToOpen, force=False, multiLine=False, separator="" ):
		try:
			file = open( fileToOpen, "r", encoding="utf-8" )
		except:
			print( "IN fileIO::simpleRead: could not open file <", fileToOpen, ">" )
			if( force ):
				self.forceCreate( fileToOpen )
				return ''
			else:
				return ''
		if( separator == "" and multiLine == False ):
			data = file.read( )
			file.close( )
			return data
		elif( separator != "" and multiLine == True ):
			separated = []
			for item in file.read( ).splitlines( ):
				if( item != '' ):
					separated.append( item.split( separator ))
			file.close( )
			return list( filter( None, separated ))
				
		elif( separator != "" ):
			data = file.read( ).split( separator )
			file.close( )
			return list( filter( None, data ))
		elif( multiLine == True ):
			data = file.read( ).splitlines( )
			file.close( )
			return list( filter( None, data ))

	def conditionalQtRead( self, fileToOpen, listOfQtItems, force=False, returnText=False ):
		i = 0
		try:
			file = open( fileToOpen, "r", encoding="utf-8")
		except:
			print( "IN fileIO::conditionalQtRead: could not open file <", fileToOpen, ">" )
			if( force ):
				self.forceCreate( fileToOpen )
			else:
				return -1
		data = file.read( ).splitlines( )
		for d in data:
			for item in listOfQtItems:
				if( d == item.text( ) and len( item.text( ))):
					item.setChecked( True )
					i += 1 
		if( returnText ):
			return data
		else:
			return i

	def simpleWrite( self, fileToOpen, text, newLine=False, clearContents=True ):
		nl = ''
		if( newLine == True ):
			nl = '\n'
		file = open( fileToOpen, "a+", encoding="utf-8" )

		if( clearContents ):
			file.truncate( 0 )
		if( type( text ) is list ):	
			for i, t in enumerate( text ):
				if( i == len( text )):
					file.write( t )
				else:
					file.write( t + nl )
		else:
			file.write( str( text + nl ))

		file.close( )

	def conditionalQtWrite( self, fileToOpen, listOfQtItems, newLine=False, clearContents=True ):
		nl = ''
		if( newLine == True ):
			nl = '\n'
		file = open( fileToOpen, "a+", encoding="utf-8" )

		if( clearContents ):
			file.truncate( 0 )
		for item in listOfQtItems:
			if( item.isChecked( ) and len( item.text( ))):
				file.write( item.text( ) + nl )

		file.close( )

	def conditionalWrite( self, fileToOpen, dictionary, clearContents=True, separator='',newLine=False ):
		i = 0
		nl=''
		if( len( dictionary ) == 0 ):
			print( "IN fileIO::conditionalWrite: dictionary must have at least one element.")
			return -1
		file = open( fileToOpen, "a+", encoding="utf-8" )

		if( clearContents ):
			file.truncate( 0 )
		if( newLine ):
			nl = "\n"
		for i, item in enumerate( dictionary ):
			if( item[ 'Bool' ]):
				if( i == len( dictionary )):
					file.write( str( item[ 'Data' ]) + separator )
				else:
					file.write( str( item[ 'Data' ]) + separator + nl )
				i += 1
		file.close( )
		return i

	def separateTwoStrings( self, text1, text2, separator ):
		if( len( text1 ) != len( text2 )):
			print( "IN fileIO::separateTwoStrings: text1 and text2 must be the same length" )
			return -1
		text = []
		for i in range( len( text1 )):
			text.append( text1[ i ] + separator + text2[ i ] )
		return text

	def makePath( self, path ):
		splitPath = path.split( "/" )
		fullPath = ''
		for i in range( len( splitPath )):
			fullPath += splitPath[ i ] + '/'
			if( i == len( splitPath ) -1 and "." in splitPath[ i ] and not Path( fullPath ).exists( )):
				Path( fullPath ).touch( )
			if( not Path( fullPath ).exists( )):
				os.mkdir( fullPath )
		return path


	def removeNthLine( self, fileToOpen, n ):
		for line in fileinput.input( fileToOpen, inplace=1 ):
			if( fileinput.lineno( ) == n+1 ):
				continue
			else:
				print( line, end='' )

		fileinput.close( )
		#return self.delEmptyFile( fileToOpen )

	def forceCreate( self, fileToOpen ):
		print( "Forcing to make <", fileToOpen, ">" )
		file = open( fileToOpen, "w" )
		file.close( )

	def clearFile( self, fileToOpen ):
		file = open( fileToOpen, "w" )
		file.close( )

	def formListOfDictionary( self, listOfBools, listOfData ):
		dictionary = []
		if( len( listOfBools ) == len( listOfData )):
			for i in range( len( listOfBools )):
				dictionary.append({ 'Bool' : listOfBools[ i ], 'Data' : listOfData[ i ]})
			return dictionary
		else:
			print( "IN fileIO::formListOfDictionary: listOfBools and listOfData must have the same length" )
			return -1

	def formListOfQtDictionary( self, listOfQt, rng=-1 ):
		dictionary = []
		if( rng == -1 ):
			rng = len( listOfQt )
		for i in range( rng ):
			dictionary.append({ 'Bool' : listOfQt[ i ].isChecked( ), 'Data' : listOfQt[ i ].text( )})
		return dictionary

	def delEmptyFile( self, fileToDel ):
		if( os.path.getsize( fileToDel ) == 0 ):
			os.remove( fileToDel )
			return 1
		return 0

	def fileExists( self, fileToFind ):
		if( Path( fileToFind ).exists( )):
			return True
		else:
			return False

	def getNumOfLines( self, file ):
		try:
			f = open( file, 'r', encoding="utf-8" )
			return len( list( filter( None, f.read( ).splitlines( ))))
		except:
			#print( "IN fileIO::getNumOfLines: could not open file <", file, ">" )
			return 0
		