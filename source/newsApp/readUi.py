from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QWidget

class readUi(QWidget):
    def __init__( self, x, y, columnCount ):
        super( ).__init__( )
        self.setupUi( x, y, columnCount )

    def setupUi(self, x, y, columnCount ):
        self.setObjectName("Form")
        self.setFixedSize(x, y)
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, x, y))
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount( columnCount )
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        
        self.tableWidget.verticalHeader().setSectionResizeMode( QtWidgets.QHeaderView.ResizeToContents )
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)

        self.tableWidget.setHorizontalHeaderLabels(["News Titles"])

        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "News"))
        self.tableWidget.setSortingEnabled(False)