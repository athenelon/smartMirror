from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

class newsUi(QWidget):
	__categoryNames = [ "Business", "General", "Health", "Science",
						"Sports", "Entertainment", "Technology" ]

	def __init__( self, x, y, soruceCount ):
		super( ).__init__( )
		self.setupUi( x, y, soruceCount )

	def setupUi(self, x, y, soruceCount):
		self.setObjectName("editNewsWidget")
		self.setFixedSize(x, y)
		self.categoryGroupBox = QtWidgets.QGroupBox(self)
		self.categoryGroupBox.setGeometry(QtCore.QRect(190, 10, 161, 201))
		self.categoryGroupBox.setObjectName("categoryGroupBox")

		self.allCheckBox = QtWidgets.QCheckBox(self.categoryGroupBox)
		self.allCheckBox.setGeometry(QtCore.QRect(10, 30, 92, 23))
		self.allCheckBox.setTristate(True)
		self.allCheckBox.setObjectName("allCheckBox")
		self.newsScrollArea = QtWidgets.QScrollArea(self)
		self.newsScrollArea.setGeometry(QtCore.QRect(10, 70, 171, 171))
		self.newsScrollArea.setMinimumSize(QtCore.QSize(171, 171))
		self.newsScrollArea.setMaximumSize(QtCore.QSize(171, 20000))
		self.newsScrollArea.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.newsScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.newsScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.newsScrollArea.setWidgetResizable(True)
		self.newsScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
		self.newsScrollArea.setObjectName("newsScrollArea")
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 169, 169))
		self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
		self.verticalLayout.setObjectName("verticalLayout")
		self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		self.label_2.setMaximumSize(QtCore.QSize(300, 30))
		self.label_2.setObjectName("label_2")
		self.verticalLayout.addWidget(self.label_2)
		self.newsScrollArea.setWidget(self.scrollAreaWidgetContents)
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(10, 10, 67, 16))
		self.label.setObjectName("label")
		self.comboBox = QtWidgets.QComboBox(self)
		self.comboBox.setGeometry(QtCore.QRect(50, 40, 131, 25))
		self.comboBox.setObjectName("comboBox")
		self.buttonBox = QtWidgets.QDialogButtonBox(self)
		self.buttonBox.setGeometry(QtCore.QRect(190, 220, 161, 21))
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
		self.buttonBox.setObjectName("buttonBox")
		self.allCheckBox2 = QtWidgets.QCheckBox(self)
		self.allCheckBox2.setGeometry(QtCore.QRect(10, 40, 41, 23))
		self.allCheckBox2.setTristate(True)
		self.allCheckBox2.setObjectName("allCheckBox2")


		self.comboBox.addItem("")
		self.comboBox.addItem("")
		self.comboBox.addItem("")
		self.comboBox.addItem("")
		self.comboBox.addItem("")
		self.comboBox.addItem("")
		self.comboBox.addItem("")

		self.progressBar = QtWidgets.QProgressBar( self )
		self.progressBar.setGeometry(QtCore.QRect(190, 220, 161, 21))
		self.progressBar.hide( )

		#sources checkBoxes
		self.sourceCheckBox = [] 
		for i in range( soruceCount ):
			self.sourceCheckBox.append( QtWidgets.QCheckBox( self.newsScrollArea ))
			self.sourceCheckBox[ i ].setObjectName("sourceCheckBox" + str( i ))
			self.sourceCheckBox[ i ].setGeometry( -10, -10, 0, 0 )
			self.verticalLayout.addWidget( self.sourceCheckBox[i] )

		#Category checkBoxes
		self.categoryCheckBox = []
		for i in range( 7 ):
			self.categoryCheckBox.append( QtWidgets.QCheckBox( self.categoryGroupBox ))
			self.categoryCheckBox[ i ].setObjectName( "categoryCheckBox" + str( i ))
			self.categoryCheckBox[ i ].setGeometry( QtCore.QRect( 30 , 50 + 20*i, 121, 23 ))


		self.retranslateUi(self)
		QtCore.QMetaObject.connectSlotsByName(self)

	def retranslateUi(self, editNewsWidget):
		_translate = QtCore.QCoreApplication.translate
		editNewsWidget.setWindowTitle(_translate("editNewsWidget", "Edit News"))
		self.categoryGroupBox.setTitle(_translate("editNewsWidget", "Category"))
		self.allCheckBox.setText(_translate("editNewsWidget", "All"))
		self.label_2.setText(_translate("editNewsWidget", "No sources available"))
		self.label.setText(_translate("editNewsWidget", "Country:"))
		self.allCheckBox2.setText(_translate("editNewsWidget", "All"))

		self.comboBox.setItemText(0, _translate("editNewsWidget", "World Wide"))
		self.comboBox.setItemText(1, _translate("editNewsWidget", "Serbia"))
		self.comboBox.setItemText(2, _translate("editNewsWidget", "United Kingdom"))
		self.comboBox.setItemText(3, _translate("editNewsWidget", "United States"))
		self.comboBox.setItemText(4, _translate("editNewsWidget", "Russia"))
		self.comboBox.setItemText(5, _translate("editNewsWidget", "Greece"))
		self.comboBox.setItemText(6, _translate("editNewsWidget", "China"))

		for box in self.sourceCheckBox:
			box.setText( _translate( "scrollAreaWidgetContents", ""))
			
		for i, box in enumerate( self.categoryCheckBox ):
			box.setText( _translate( "scrollAreaWidgetContents", self.__categoryNames[i] ))