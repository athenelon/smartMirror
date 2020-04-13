from PyQt5 import QtCore

class qtBasics:
	#def __init__( self ):
		#self.quitSignalExit = QtCore.pyqtSignal( int )

	def show( self, xPos, yPos ):
		self.move( xPos, yPos )
		self.setVisible( True )
		print( "called")

	def closeEvent( self, event ):
		self.setVisible( False )
		self.quitSignalExit.emit( 1 )