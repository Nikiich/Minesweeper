from PyQt6.QtCore import QRect
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QLabel, QPushButton

from BackToMenuDialog import BackToMenuDialog
from NewGameDialog import NewGameDialog
from ResultsWidget import ResultsWidget
from database import get_all_results

FONT_1 = QFont()
FONT_1.setFamily("Copperplate Gothic Bold")
FONT_1.setPointSize(16)
FONT_2 = QFont()
FONT_2.setFamily("Copperplate Gothic Bold")
FONT_2.setPointSize(48)
FONT_2.setBold(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minesweeper")
        self.setWindowIcon(QIcon('icons/mine.png'))
        self.setFixedSize(720, 480)
        self.game_widget = None
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.main_widget = QWidget()
        self.main_widget.setStyleSheet("background-color:#B0BFD7")
        self.game_name_label = QLabel("Mine Sweeper", parent=self.main_widget)
        self.game_name_label.setGeometry(QRect(110, 70, 515, 50))
        self.game_name_label.setFont(FONT_2)
        self.new_game_button = QPushButton("New Game", parent=self.main_widget)
        self.new_game_button.setGeometry(QRect(195, 170, 330, 80))
        self.new_game_button.setFont(FONT_1)
        self.new_game_button.setStyleSheet("background-color:#8296B4")
        self.scores_button = QPushButton("Scores", parent=self.main_widget)
        self.scores_button.setStyleSheet("background-color:#8296B4")
        self.scores_button.setFont(FONT_1)
        self.scores_button.setGeometry(QRect(195, 280, 330, 80))
        self.scores_button.clicked.connect(self.switch_to_score_page)
        self.new_game_button.clicked.connect(self.show_new_game_dialog)
        self.stack.setStyleSheet("background-color:#8296B4")
        self.stack.addWidget(self.main_widget)
        self.pause_menu_widget = QWidget()
        self.continue_btn = QPushButton('Continue', parent=self.pause_menu_widget)
        self.continue_btn.setGeometry(QRect(200, 140, 330, 80))
        font = QFont()
        font.setFamily("Copperplate Gothic Bold")
        font.setPointSize(16)
        self.continue_btn.setFont(font)
        self.continue_btn.setStyleSheet("background-color:#B0BFD7\n")
        self.continue_btn.clicked.connect(self.switch_to_game_page)
        self.back_to_menu_btn = QPushButton('Back to menu', parent=self.pause_menu_widget)
        self.back_to_menu_btn.setGeometry(QRect(200, 260, 330, 80))
        self.back_to_menu_btn.setFont(font)
        self.back_to_menu_btn.setStyleSheet("background-color:#B0BFD7\n")
        self.back_to_menu_btn.clicked.connect(self.go_to_main_menu)
        self.stack.addWidget(self.pause_menu_widget)
        self.scores_page_widget = ResultsWidget(get_all_results())
        self.scores_page_widget.switch_to_main_page.connect(self.switch_to_main_page)
        self.stack.addWidget(self.scores_page_widget)

    def show_new_game_dialog(self):
        dialog = NewGameDialog(self)
        dialog.exec()

    def go_to_main_menu(self):
        back_to_menu_dialog = BackToMenuDialog(self)
        back_to_menu_dialog.switch_to_main_menu.connect(self.switch_to_main_page)
        back_to_menu_dialog.exec()

    def switch_to_main_page(self):
        self.stack.setCurrentWidget(self.main_widget)

    def switch_to_pause_menu(self):
        self.stack.setCurrentWidget(self.pause_menu_widget)

    def switch_to_game_page(self):
        self.stack.setCurrentWidget(self.game_widget)

    def switch_to_score_page(self):
        self.scores_page_widget.update_results(get_all_results())
        self.stack.setCurrentWidget(self.scores_page_widget)
