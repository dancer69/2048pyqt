from PyQt5 import QtCore
from PyQt5.QtCore import Qt

GRID_LEN = 4
SCORE=0
HISCORE=0

CELL_IMAGE_DICT={"empty": "/resources/images/tileBack.png", 2: "/resources/images/2.png",4: "/resources/images/4.png",8: "/resources/images/8.png", 16: "/resources/images/16.png",
                  32: "/resources/images/32.png",64: "/resources/images/64.png",128: "/resources/images/128.png",256: "/resources/images/256.png",
                  512: "/resources/images/512.png",1024: "/resources/images/1024.png",2048: "/resources/images/2048.png", 4096: "/resources/images/4096.png",
                  8192: "/resources/images/8192.png", 16384: "/resources/images/16384.png", 32768: "/resources/images/32768.png", 65536: "/resources/images/65536.png"}

SOUNDS_DICT={"2048":"/resources/sounds/claps.wav", "4096": "/resources/sounds/eehh.wav", "8192": "/resources/sounds/ooo.wav",
              "16384": "/resources/sounds/yee.wav", "32768": "/resources/sounds/wow.wav", "65535": "/resources/sounds/omg.wav",
              "move": "/resources/sounds/move.wav", "lose": "/resources/sounds/lose.wav"}

KEY_UP_ALT = QtCore.Qt.Key_Up
KEY_DOWN_ALT = QtCore.Qt.Key_Down
KEY_LEFT_ALT = QtCore.Qt.Key_Left
KEY_RIGHT_ALT = QtCore.Qt.Key_Right
KEY_BACK_ALT= QtCore.Qt.Key_Z

KEY_UP = QtCore.Qt.Key_W
KEY_DOWN = QtCore.Qt.Key_S
KEY_LEFT = QtCore.Qt.Key_A
KEY_RIGHT = QtCore.Qt.Key_D
KEY_BACK = QtCore.Qt.Key_Backspace


KEY_I = QtCore.Qt.Key_I
KEY_K = QtCore.Qt.Key_K
KEY_J = QtCore.Qt.Key_J
KEY_L = QtCore.Qt.Key_L
