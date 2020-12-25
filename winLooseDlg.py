import os

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap, QCursor
from PyQt5.QtWidgets import QDialog
import logic

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
winLooseDlg_ui=APP_FOLDER + "/winLooseDlg.ui"
#winLooseDlg_ui=r"/home/useful/python-workspace/2048pyqt/winLooseDlg.ui"
Ui_winLooseDlg, _=  QtBaseClass=uic.loadUiType(winLooseDlg_ui, resource_suffix="")

class WinLooseDialog(QDialog, Ui_winLooseDlg):
    def __init__(self, parent=None):

        super(WinLooseDialog,self).__init__(parent, flags=QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.bOk.hide()

        self.parent = parent
        self.fontDatabase = QFontDatabase()
        self.fontDatabase.addApplicationFont(APP_FOLDER + "/resources/fonts/JackportCollegeNcv-1MZe.ttf")
        self.fontDatabase.addApplicationFont(APP_FOLDER + "/resources/fonts/Rosemary-Bold.ttf")
        self.lWinLoose.setFont(QFont("JACKPORT COLLEGE NCV", 72))
        self.lAsk.setFont(QFont("Rosemary", 27))
        self.lWinNumber.setFont(QFont("JACKPORT COLLEGE NCV", 33))
        self.bNo.setFont(QFont("JACKPORT COLLEGE NCV", 36))
        self.bYes.setFont(QFont("JACKPORT COLLEGE NCV", 36))
        self.bNo.clicked.connect(self.bNoClicked)
        self.bYes.clicked.connect(self.bYesClicked)
        self.bOk.clicked.connect(self.bOkClicked)
        handCurImg = QPixmap(APP_FOLDER + "/resources/images/handCursor.png")
        self.window().setCursor(QCursor(handCurImg,15,2))

    def dialogTypes(self, dlgtype):
        if dlgtype == "WIN":
            self.lWinLoose.setText("ΚΕΡΔΙΣΑΤΕ ! ! !")
            self.lAsk.setText("Θέλετε να συνεχίσετε;")
            self.lWinBack.show()
            self.lWinNumber.show()
            self.lWinNumber.setNum(logic.winNum)
            self.exec()
        elif dlgtype == "LOOSE":
            self.lWinLoose.setText("ΧΑΣΑΤΕ :)")
            self.lAsk.setText("Θέλετε να ξεκινήσετε νέο παιχνίδι; \nΠατώντας όχι μπορείτε να αναιρέσετε την τελευταία \nσας ενέργεια(ή περισσότερες) και να συνεχίσετε.")
            self.lWinBack.hide()
            self.lWinNumber.hide()
            self.exec()
        elif dlgtype == "ENDGAME":
            self.lWinLoose.setText("ΜΠΡΑΒΟ ! ! !")
            self.lAsk.setText("Ολοκληρώσατε το παιχνίδι!")
            self.bNo.hide()
            self.bYes.hide()
            self.bOk.show()
            self.exec()

        elif dlgtype == "HIDE":
            self.close()

    defVal=logic.winNum
    print(defVal)

    def bYesClicked(self):
        if self.lWinLoose.text()== "ΚΕΡΔΙΣΑΤΕ ! ! !":
            print("hide")
            logic.winNum=logic.winNum*2
            print(logic.winNum)
            self.dialogTypes("HIDE")
        elif self.lWinLoose.text()== "ΧΑΣΑΤΕ :)":
            self.parent.on_bPlay_clicked()
            self.dialogTypes("HIDE")

    def bNoClicked(self):
        if self.lWinLoose.text() == "ΚΕΡΔΙΣΑΤΕ ! ! !":
            logic.winNum = self.defVal
            print(self.defVal)
            self.parent.on_bPlay_clicked()
            self.dialogTypes("HIDE")
        else:
            self.dialogTypes("HIDE")

    def bOkClicked(self):
        logic.winNum = self.defVal
        self.parent.on_bPlay_clicked()
        self.bYes.show()
        self.bNo.show()
        self.bOk.hide()
        self.dialogTypes("HIDE")