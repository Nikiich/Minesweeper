from PyQt6.QtCore import pyqtSignal, QRect, QSize, Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton


class BackToMenuDialog(QDialog):
    switch_to_main_menu = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 200)
        self.setStyleSheet('Background-color: #B0BFD7')
        self.label = QLabel('The progress will be lost.\nDo you want to stop the game?', parent=self)
        self.label.setGeometry(QRect(10, 20, 381, 81))
        font = QFont()
        font.setFamily("Copperplate Gothic Bold")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.yes_btn = QPushButton(parent=self)
        self.yes_btn.setGeometry(QRect(55, 120, 130, 50))
        self.yes_btn.setStyleSheet("background-color:#8296B4 ")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/yes.svg"), QIcon.Mode.Normal, QIcon.State.Off)
        self.yes_btn.setIcon(icon)
        self.yes_btn.setIconSize(QSize(40, 40))
        self.yes_btn.clicked.connect(self.go_to_menu)
        self.no_btn = QPushButton(parent=self)
        self.no_btn.setGeometry(QRect(215, 120, 130, 50))
        self.no_btn.setStyleSheet("background-color:#8296B4 ")
        self.no_btn.clicked.connect(self.close)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("icons/no.svg"), QIcon.Mode.Normal, QIcon.State.Off)
        self.no_btn.setIcon(icon1)
        self.no_btn.setIconSize(QSize(40, 40))

    def go_to_menu(self):
        self.close()
        self.switch_to_main_menu.emit()
