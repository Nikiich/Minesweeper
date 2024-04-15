from PyQt6.QtCore import QRegularExpression, QSize, QRect
from PyQt6.QtGui import QFont, QRegularExpressionValidator, QIcon
from PyQt6.QtWidgets import QDialog, QPushButton, QFrame, QLabel, QLineEdit, QComboBox, QVBoxLayout, QMessageBox

from GameWidgets import DiffLvl, GameWidget
from database import create_user, authenticate_user, if_exists_by_name


class NewGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Game")
        self.setFixedSize(QSize(250, 270))
        self.setStyleSheet("background-color:#B0BFD7")
        self.user = None
        font = QFont()
        font.setFamily("Copperplate Gothic Bold")
        font.setPointSize(12)
        self.start_button = QPushButton("Start")
        self.start_button.setFixedSize(QSize(210, 40))
        self.start_button.setFont(font)
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setStyleSheet("background-color:#8296B4")
        self.frame = QFrame(self)
        self.frame.setGeometry(QRect(10, 40, 230, 220))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setStyleSheet('Background-color: #B0BFD7')
        self.new_game_label = QLabel('New game:', self)
        self.new_game_label.setFont(font)
        self.new_game_label.setGeometry(QRect(10, 7, 100, 30))
        self.nickname_label = QLabel("Nickname:", self.frame)
        regex = QRegularExpression(r'^[a-zA-Z0-9._]+$')
        self.nickname_validator = QRegularExpressionValidator(regex)
        self.nickname_label.setFont(font)
        self.nickname_edit = QLineEdit(self.frame)
        self.nickname_edit.setFont(font)
        self.nickname_edit.setStyleSheet("Background-color: white")
        self.nickname_edit.setValidator(self.nickname_validator)
        self.password_label = QLabel('Password:', self.frame)
        self.password_label.setFont(font)
        self.password_edit = QLineEdit(self.frame)
        self.password_edit.setFont(font)
        self.password_edit.setStyleSheet("Background-color: white")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.difficulty_label = QLabel("Difficulty:", self.frame)
        self.difficulty_label.setFont(font)
        self.difficulty_combo = QComboBox(self.frame)
        self.difficulty_combo.setStyleSheet("Background-color: white")
        self.difficulty_combo.addItem('Beginner')
        self.difficulty_combo.addItem('Intermediate')
        self.difficulty_combo.addItem('Expert')
        self.difficulty_combo.setFont(font)
        self.frame_layout = QVBoxLayout()
        self.frame_layout.addWidget(self.nickname_label)
        self.frame_layout.addWidget(self.nickname_edit)
        self.frame_layout.addWidget(self.password_label)
        self.frame_layout.addWidget(self.password_edit)
        self.frame_layout.addWidget(self.difficulty_label)
        self.frame_layout.addWidget(self.difficulty_combo)
        self.frame_layout.addWidget(self.start_button)
        self.frame.setLayout(self.frame_layout)

    def start_game(self):
        if len(self.nickname_edit.text()) < 4:
            self.show_message('Nickname must be longer than 3 characters')
            return
        if len(self.password_edit.text()) < 6:
            self.show_message('Password must be longer than 6 characters')
            return
        user_exists = if_exists_by_name(self.nickname_edit.text())
        if user_exists:
            self.user = authenticate_user(self.nickname_edit.text(), self.password_edit.text())
            if self.user is not None:
                self.show_message("Successfully logged")
            else:
                self.show_message("Incorrect password")
                return
        else:
            self.user = create_user(self.nickname_edit.text(), self.password_edit.text())
            self.show_message("Successfully registered")

        level = self.difficulty_combo.currentText()
        game_widget = GameWidget(DiffLvl(level), self.parent(), self.user)
        game_widget.switch_to_pause_menu.connect(self.parent().switch_to_pause_menu)
        self.parent().stack.addWidget(game_widget)
        self.parent().stack.setCurrentWidget(game_widget)
        self.parent().game_widget = game_widget
        self.close()

    def show_message(self, text):
        msg = QMessageBox()
        msg.setFixedSize(400, 200)
        msg.setStyleSheet('Background-color: #B0BFD7')
        msg.setWindowTitle("Message")
        font = QFont()
        font.setFamily('Copperplate Gothic Bold')
        font.setPointSize(15)
        msg.setFont(font)
        msg.setText(text)

        yes_btn = QPushButton(msg)
        yes_btn.setGeometry(QRect(135, 125, 130, 50))
        yes_btn.setStyleSheet("background-color: #8296B4")
        icon = QIcon("icons/yes.svg")
        yes_btn.setIcon(icon)
        yes_btn.setIconSize(QSize(40, 40))
        yes_btn.setDefault(True)
        yes_btn.clicked.connect(msg.accept)
        msg.addButton(yes_btn, QMessageBox.ButtonRole.ActionRole)
        msg.exec()
