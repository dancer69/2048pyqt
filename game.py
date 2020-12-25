import os
import random
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSettings, Qt, QPoint, QByteArray, QSize
from PyQt5.QtGui import QFontDatabase, QFont, QMovie, QPixmap, QCursor
from PyQt5.QtWidgets import QMainWindow, QLabel
from game2048 import Ui_MainWindow
import constants as c
import logic
import pygame
import winLooseDlg
import helpDlg
from pixstyle import RoundPixmapStyle
import moosegesture

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))

#Δημιουργία τυχαίων νέων πλακιδίων στο πλαίσιο
def gen():
    return random.randint(0, c.GRID_LEN - 1)

class Game(QMainWindow, Ui_MainWindow):
    # set window on screen center
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(
            QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    # move window by holding right mouse button
    def mousePressEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        # print(delta)
        if event.buttons() == Qt.RightButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def animateBackground(self):
        # Load the file into a QMovie
        self.movie = QMovie(APP_FOLDER + "/resources/images/clouds.gif", QByteArray(), self)
        self.movie.setScaledSize(QSize(1020,900))
        self.movie.setSpeed(70)
        proxy_style = RoundPixmapStyle(radius=20, style=self.lbBackground.style())
        self.lbBackground.setStyle(proxy_style)
        self.lbBackground.setMovie(self.movie)
        self.movie.start()

    def settings(self):
        settings = QSettings()
        return settings

    def __init__(self, parent=None):
        #Αρχικοποίηση του γραφικού περιβάλλοντος
        super(Game,self).__init__(parent)
        print(APP_FOLDER)
        self.setupUi(self)

        #Μεταβλητές
        self.points=[]
        self.speed=30
        self.movie = None
        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left, c.KEY_RIGHT_ALT: logic.right,
                         c.KEY_J: logic.left, c.KEY_L: logic.right,
                         c.KEY_I: logic.up, c.KEY_K: logic.down}

        self.setWindowFlags(
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.center()

        self.settings()
        self.restoreStates()

        self.fontDatabase = QFontDatabase()
        self.fontDatabase.addApplicationFont(APP_FOLDER + "/resources/fonts/JackportCollegeNcv-1MZe.ttf")
        self.fontDatabase.addApplicationFont(APP_FOLDER + "/resources/fonts/Rosemary-Bold.ttf")
        self.lScore.setFont(QFont("JACKPORT COLLEGE NCV", 40))
        self.lHiScore.setFont(QFont("JACKPORT COLLEGE NCV", 40))
        self.bExit.setFont(QFont("JACKPORT COLLEGE NCV", 32))
        self.lMediaSet.setFont(QFont("Rosemary", 38))
        swipeCurImg = QPixmap(APP_FOLDER + "/resources/images/swipeCursor.png")
        handCurImg = QPixmap(APP_FOLDER + "/resources/images/handCursor.png")
        self.cursors = [handCurImg, swipeCurImg]
        self.centralwidget.setCursor(QCursor(self.cursors[0], 15, 2))
        self.frame.setCursor(QCursor(self.cursors[1], 35, 35))
        self.frame.setAttribute(Qt.WA_StyledBackground, (True))
        self.animateBackground()
        self.musIcon()
        self.sndIcon()
        self.playMusic()

        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()

        #Αντιστοίχιση ενεργειών κίνησης ποντικιού και κλικ
        self.bHelp.clicked.connect(self.bHelpClicked)
        self.bAnim.clicked.connect(self.animStartStop)
        self.sndslider.valueChanged.connect(self.sndslvalchanged)
        self.musslider.valueChanged.connect(self.musslvalchanged)
        self.frame.installEventFilter(self)

    #Μέθοδος ενεργοποίησης/απενεργοποίησης του κινούμενου bakcground
    def animStartStop(self):
        if self.movie!=None and self.movie.state()==QMovie.Running:
            self.movie.stop()
            self.bAnim.setStyleSheet("QPushButton{\n"
                                      "border-image: url(:/resources/images/anim_off.png)\n"
                                        "}")
        else:
            self.animateBackground()
            self.bAnim.setStyleSheet("QPushButton{\n"
                                     "border-image: url(:/resources/images/anim_on.png)\n"
                                     "}")


    #Σχεδίαση του βασικού πλαισίου
    def init_grid(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                self.gridBoard.addWidget(self.setTile("empty"), i,j)

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.replaceTile("empty", i, j)
                else:
                    self.replaceTile(new_number, i,j)

    # Δημιουργία των αριθμητικών πλακιδίων
    def setTile(self, item):
        tile = QLabel('')
        tile.setFocusPolicy(Qt.NoFocus)
        tile.setFixedWidth(135)
        tile.setFixedHeight(140)
        path = c.CELL_IMAGE_DICT.get(item)
        tile.setStyleSheet("QLabel{\n"
                           "border-image: url(:" + str(path) + ")\n"
                                                               "}")
        return tile

    #Μέθοδος αντικατάστασης πλακιδίου
    def replaceTile(self,newTile, pX,pY):
        item = self.gridBoard.itemAtPosition(pX, pY)
        self.gridBoard.removeWidget(item.widget())
        self.gridBoard.addWidget(self.setTile(newTile), pX, pY)

    #Ενεργοποίηση των πλήκτρων χειρισμού
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            if key == QtCore.Qt.Key_Home:
                #print("is up!")
                if self.frameGeometry().y() > 0:
                    self.move(self.frameGeometry().x(), self.frameGeometry().y() - self.speed)
            elif key == QtCore.Qt.Key_End:
                #print("is down!")
                if self.frameGeometry().y() > 0:
                    self.move(self.frameGeometry().x(), self.frameGeometry().y() + self.speed)
            elif key == QtCore.Qt.Key_Delete:
                #print("is left!")
                if self.frameGeometry().x() > 0:
                    self.move(self.frameGeometry().x() - self.speed, self.frameGeometry().y())
            elif key == QtCore.Qt.Key_PageDown:
                #print("is right!")
                if self.frameGeometry().x() > 0:
                    self.move(self.frameGeometry().x() + self.speed, self.frameGeometry().y())
        if key == c.KEY_BACK or key==c.KEY_BACK_ALT:
            if len(self.history_matrixs) > 1:
                self.matrix = self.history_matrixs.pop()
                self.update_grid_cells()
                print('back on step total step:', len(self.history_matrixs))

        #Έλεγχος Αν το παιχνίδι τελείωσε και αν έχει κερδηθεί ή χαθεί
        elif key in self.commands:
            self.frame.setCursor(Qt.BlankCursor)
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.stateOfGame()

    def stateOfGame(self):
        self.playSound(APP_FOLDER + c.SOUNDS_DICT["move"])
        self.matrix = logic.add_two(self.matrix)
        # record last move
        self.history_matrixs.append(self.matrix)
        self.update_grid_cells()
        if logic.game_state(self.matrix) == 'win':
            if logic.winNum != 65535:
                print("num: " + str(logic.winNum))
                for key, value in c.SOUNDS_DICT.items():
                    if key == str(logic.winNum):
                        self.playSound(APP_FOLDER + value)
                winLooseDlg.WinLooseDialog(self).dialogTypes("WIN")
                print("Κερδίσες")
            else:
                winLooseDlg.WinLooseDialog(self).dialogTypes("ENDGAME")
        if logic.game_state(self.matrix) == 'lose':
            self.playSound(APP_FOLDER + c.SOUNDS_DICT["lose"])
            winLooseDlg.WinLooseDialog(self).dialogTypes("LOOSE")
            print("Έχασες")
        self.lScore.setText(str(c.SCORE))
        if int(self.lHiScore.text()) < int(self.lScore.text()):
            self.lHiScore.setText(self.lScore.text())

    #Μέθοδος για χειρσμό με κλικ και σύρσιμο του ποντικιού
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            self.frame.setCursor(QCursor(self.cursors[1], 35, 35))
            if event.buttons() == QtCore.Qt.LeftButton:

                if len(self.points) > 2:
                    startx, starty = self.points[0][0], self.points[0][1]
                    for i in range(len(self.points)):
                        self.points[i] = (self.points[i][0] - startx, self.points[i][1] - starty)
                self.points.append((event.localPos().x(), event.localPos().y()))
                #print(self.points)
        if event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            #print("Released!")
            self.mouseDown = False
            strokes = moosegesture.getGesture(self.points)
            strokeText=str(strokes[-1])
            #print(strokeText)
            if strokeText == "R":
                self.matrix, done = logic.right(self.matrix)
                if done:
                    self.stateOfGame()
            elif strokeText == "L":
                self.matrix, done = logic.left(self.matrix)
                if done:
                    self.stateOfGame()
            elif strokeText == "U":
                self.matrix, done = logic.up(self.matrix)
                if done:
                    self.stateOfGame()
            elif strokeText == "D":
                self.matrix, done = logic.down(self.matrix)
                if done:
                    self.stateOfGame()
            strokes.clear()
        else:
            return True

        return self.frame.eventFilter(source, event)

    #Μέθοδος για την αναπαραγωγή των ήχων
    def playSound(self, sound):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=3, buffer=512)
        pygame.mixer.init()
        effect = pygame.mixer.Sound(sound)
        self.sndslider.setMinimum(0)
        self.sndslider.setMaximum(100)
        vol = self.sndslider.value()
        effect.set_volume(vol / 100)
        pygame.mixer.find_channel().play(effect)

    #Έλεγχος για αλλαγές στο εικονίδιο ήχου
    def sndslvalchanged(self):
        self.sndIcon()

    #Αλλαγή του εικονιδίου ήχου
    def sndIcon(self):
        if self.sndslider.value()==0:
            self.lSound.setStyleSheet("QLabel{\n"
                                      "border-image: url(:/resources/images/sound_off.png)\n"
                                        "}")
        else:
            self.lSound.setStyleSheet("QLabel{\n"
             "border-image: url(:/resources/images/sound_on.png)\n"
             "}")

    #Μέθοδος για την αnaπαραγωγή μουσικής
    def playMusic(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
        pygame.mixer.music.load(os.path.join(APP_FOLDER, "resources/sounds/backmusic.ogg"))
        self.musslider.setMinimum(0)
        self.musslider.setMaximum(100)
        musvol = self.musslider.value()
        pygame.mixer.music.set_volume(musvol / 100)
        pygame.mixer.music.play(loops=-1)
        self.musslider.valueChanged.connect(self.musslvalchanged)

    def musslvalchanged(self):
        pygame.mixer.music.pause()
        pygame.mixer.music.set_volume(self.musslider.value() / 100)
        pygame.mixer.music.unpause()
        self.musIcon()

    def musIcon(self):
        if self.musslider.value()==0:
            self.lMusic.setStyleSheet("QLabel{\n"
                                      "border-image: url(:/resources/images/music_off.png)\n"
                                        "}")
        else:
            self.lMusic.setStyleSheet("QLabel{\n"
             "border-image: url(:/resources/images/music_on.png)\n"
             "}")

    def bHelpClicked(self):
        helpDlg.HelpDialog(self).exec()

    pyqtSlot()
    def on_bPlay_clicked(self):
        self.gridBoard.blockSignals(False)
        self.init_grid()
        c.SCORE=0
        self.lScore.setText(str(c.SCORE))
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()


    pyqtSlot()
    def on_bExit_clicked(self):
        self.saveStates()
        self.movie.jumpToFrame(100)
        sys.exit()

    # αποθήκευση τιμών της εφαρμογής
    def saveStates(self):
        self.settings().setValue("slidervalue", self.sndslider.value())
        self.settings().setValue("sliderMvalue", self.musslider.value())
        self.settings().setValue("HighScore", self.lHiScore.text())
        self.settings().setValue("geometry", self.saveGeometry())
        self.settings().setValue("windowState", self.saveState())
        self.settings().sync()

    # Επαναφορά αποθηκευμένων τιμών από το preferencies.ini
    def restoreStates(self):
        self.sndslider.setValue(self.settings().value("slidervalue", 40, type=int))
        self.musslider.setValue(self.settings().value("sliderMvalue", 50, type=int))
        self.lHiScore.setText(self.settings().value("HighScore", "0"))
        if not self.settings().value("geometry") == None:
            self.restoreGeometry(self.settings().value("geometry"))
        if not self.settings().value("windowState") == None:
            self.restoreState(self.settings().value("windowState"))

    def closeEvent(self, e):
        self.saveStates()

def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    QCoreApplication.setOrganizationName("d69soft")
    QCoreApplication.setApplicationName("2048pyqt")
    ui=Game()
    ui.show()
    return app.exec_()
