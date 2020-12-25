import os

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont, QCursor, QPixmap
from PyQt5.QtWidgets import QDialog

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
hlpDlg_ui=APP_FOLDER + "/helpDlg.ui"
#hlpDlg_ui=r"/home/useful/python-workspace/2048pyqt/helpDlg.ui"
Ui_HelpDialog, _=  QtBaseClass=uic.loadUiType(hlpDlg_ui, resource_suffix="")

class HelpDialog(QDialog, Ui_HelpDialog):
    def __init__(self, parent=None):

        super(HelpDialog,self).__init__(parent, flags=QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.parent = parent
        self.fontDatabase = QFontDatabase()
        self.fontDatabase.addApplicationFont(APP_FOLDER + "/resources/fonts/JackportCollegeNcv-1MZe.ttf")
        self.fontDatabase.addApplicationFont(APP_FOLDER + "/resources/fonts/Rosemary-Bold.ttf")
        self.Header1.setFont(QFont("JACKPORT COLLEGE NCV", 42))
        self.tePage1.setFont(QFont("Rosemary", 32))
        self.tePage2.setFont(QFont("Rosemary", 32))
        self.tePage2.hide()
        self.bBack.setFont(QFont("JACKPORT COLLEGE NCV", 34))
        self.bBack.clicked.connect(self.backClicked)
        self.bFwd.clicked.connect(self.fwdClicked)
        self.bBwd.clicked.connect(self.bwdClicked)
        handCurImg = QPixmap(APP_FOLDER + "/resources/images/handCursor.png")
        scrlCurImg = QPixmap(APP_FOLDER + "/resources/images/scrollCursor.png")
        self.window().setCursor(QCursor(handCurImg, 15, 2))
        self.tePage1.viewport().setCursor(QCursor(handCurImg, 15,2))
        self.tePage2.viewport().setCursor(QCursor(scrlCurImg, 31, 1))


    def fwdClicked(self):
        self.Header1.setText("ΧΕΙΡΙΣΜΟΣ ΠΑΙΧΝΙΔΙΟΥ")
        self.tePage1.hide()
        self.tePage2.show()

    def bwdClicked(self):
        self.Header1.setText("ΣΚΟΠΟΣ ΤΟΥ ΠΑΙΧΝΙΔΙΟΥ")
        self.tePage1.show()
        self.tePage2.hide()

    def backClicked(self):
        self.close()