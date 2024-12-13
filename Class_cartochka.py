from PyQt6.QtWidgets import QPushButton
from PyQt6 import QtGui
from PyQt6 import QtCore
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


Background_picture = resource_path("Обои.jpg")


class Cartochka(QPushButton):
    def __init__(self, picture, x, y):
        super().__init__()
        self.picture_name = picture
        self.is_reversed = False
        self.is_guessed = False
        self.choosed_first = False
        self.x = x
        self.y = y

    def reverse(self):
        if self.is_guessed:
            return
        if self.is_reversed:
            self.is_reversed = False
            self.setIcon(QtGui.QIcon(resource_path(Background_picture)))
            self.setIconSize(QtCore.QSize(100, 100))
        else:
            self.is_reversed = True
            self.setIcon(QtGui.QIcon(resource_path(self.picture_name)))
            self.setIconSize(QtCore.QSize(100, 100))
