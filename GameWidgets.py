import random
from enum import Enum
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtCore import QSize, QRect
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtWidgets import QPushButton, QGridLayout, QWidget, QLabel, QLCDNumber, QToolButton
from database import add_result

CONFIG_1 = (9, 9, 10, QSize(180, 180))
CONFIG_2 = (16, 16, 40, QSize(320, 320))
CONFIG_3 = (16, 30, 99, QSize(600, 320))
font = QFont()
font.setFamily("Copperplate Gothic Bold")
font.setPointSize(12)
font.setBold(True)
STYLESHEET_ACT_BUTTON = 'QPushButton {background-color: #B0BFD7;}'


class CellState(Enum):
    VISITED = 1
    UNVISITED = 0
    MARKED = -1


class DiffLvl(Enum):
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    EXPERT = 'Expert'


SCORES = {DiffLvl.BEGINNER: 2,
          DiffLvl.INTERMEDIATE: 4,
          DiffLvl.EXPERT: 6}


class GameWidget(QWidget):
    switch_to_pause_menu = pyqtSignal()

    def __init__(self, level: DiffLvl, paren, user):
        super().__init__()
        self.user = user
        self.gameboard_widget = QWidget(parent=self)
        self.level = level
        self.standart_ico = QIcon('icons/standard.jpg')
        self.win_ico = QIcon('icons/win.jpg')
        self.lose_ico = QIcon('icons/lose.jpg')
        if level == DiffLvl.BEGINNER:
            self.rows, self.cols, self.mines, self.size = CONFIG_1
            self.geo = QRect(270, 210, 180, 180)
        if level == DiffLvl.INTERMEDIATE:
            self.rows, self.cols, self.mines, self.size = CONFIG_2
            self.geo = QRect(200, 140, 320, 320)
        if level == DiffLvl.EXPERT:
            self.rows, self.cols, self.mines, self.size = CONFIG_3
            self.geo = QRect(60, 140, 600, 320)
        self.cells_remain = self.rows * self.cols - self.mines
        self.l = False
        self.gameboard_widget.setGeometry(self.geo)
        self.first = True
        self.timer_off = True
        self.game_is_over = False
        self.timer_lcd = QLCDNumber(parent=self)
        self.timer_lcd.setGeometry(QRect(90, 50, 180, 70))
        self.timer_lcd.setStyleSheet("background-color:#B0BFD7")
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)
        self.mines_left_label = QLabel("Mines left:", parent=self)
        self.mines_left_label.setGeometry(QRect(450, 30, 140, 16))
        font = QFont()
        font.setFamily("Copperplate Gothic Bold")
        font.setPointSize(16)
        self.timer_label = QLabel('Timer:', parent=self)
        self.timer_label.setGeometry(QRect(90, 30, 81, 16))
        self.timer_label.setFont(font)
        self.mines_left_label.setFont(font)
        self.mines_left = self.mines
        self.mines_left_lcd = QLCDNumber(parent=self)
        self.mines_left_lcd.setGeometry(QRect(450, 50, 180, 70))
        self.mines_left_lcd.setStyleSheet("background-color:#B0BFD7")
        self.mines_left_lcd.display(self.mines_left)
        self.try_again_btn = QPushButton('', parent=self)
        self.try_again_btn.setGeometry(QRect(320, 50, 80, 70))
        font.setPointSize(11)
        self.try_again_btn.setFont(font)
        self.try_again_btn.setStyleSheet("background-color:#B0BFD7")
        self.try_again_btn.clicked.connect(self.try_again)
        self.try_again_btn.setIcon(self.standart_ico)
        self.try_again_btn.setIconSize(QSize(76, 66))
        self.pause_btn = QToolButton(parent=self)
        self.pause_btn.setGeometry(QRect(10, 10, 31, 31))
        font = QFont()
        font.setFamily("Copperplate Gothic Bold")
        font.setPointSize(26)
        self.pause_btn.setFont(font)
        self.pause_btn.setAutoFillBackground(False)
        self.pause_btn.setStyleSheet("background-color:#B0BFD7\n")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/menu.svg"), QIcon.Mode.Normal, QIcon.State.Off)
        self.pause_btn.setIcon(icon)
        self.pause_btn.setIconSize(QSize(18, 18))
        self.pause_btn.clicked.connect(self.switch_to_pause)
        self.minefield = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.minefield_shadow = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[CellState.UNVISITED for _ in range(self.cols)] for _ in range(self.rows)]
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.mine_positions = None
        self.create_game_board(refresh=False)

    def start_timer(self):
        self.timer.start()

    def update_timer(self):
        time = self.timer_lcd.intValue() + 1
        self.timer_lcd.display(time)

    def stop_timer(self):
        self.timer.stop()

    def go_to_main_menu(self):
        self.parent().stack.setCurrentIndex(0)

    def switch_to_pause(self):
        self.timer_off = True
        self.stop_timer()
        self.switch_to_pause_menu.emit()

    def update_mines_left_lcd(self):
        self.mines_left_lcd.display(self.mines_left)

    def create_event(self, row, col):
        def mine_press_ivent(QMouseEvent):
            if self.game_is_over:
                return
            if self.first or self.timer_off:
                self.start_timer()
                self.timer_off = False
            but = self.buttons[row][col]
            if QMouseEvent.button() == Qt.MouseButton.LeftButton:
                if not but.icon().isNull():
                    return
                self.cell_clicked(row, col)
            elif QMouseEvent.button() == Qt.MouseButton.RightButton:
                if not but.icon().isNull():
                    self.revealed[row][col] = CellState.UNVISITED
                    but.setIcon(QIcon())
                    self.mines_left += 1
                    self.update_mines_left_lcd()
                    return
                self.revealed[row][col] = CellState.MARKED
                self.mines_left -= 1
                self.update_mines_left_lcd()
                but.setIcon(QIcon('icons/flag.png'))

        return mine_press_ivent

    def create_game_board(self, refresh):
        if not refresh:
            self.grid = QGridLayout()
            self.grid.setSpacing(0)
            self.grid.setContentsMargins(0, 0, 0, 0)

        for row in range(self.rows):
            for col in range(self.cols):
                button = QPushButton()
                button.setFont(font)
                button.mousePressEvent = self.create_event(row, col)
                button.setStyleSheet(STYLESHEET_ACT_BUTTON)
                button.setFixedSize(QSize(20, 20))
                if refresh:
                    self.grid.removeWidget(self.buttons[row][col])
                    self.grid.addWidget(button, row, col)
                self.grid.addWidget(button, row, col)
                self.buttons[row][col] = button
        self.gameboard_widget.setFixedSize(self.size)
        self.gameboard_widget.setLayout(self.grid)

    def place_mines(self, mines, row, col):
        positions = [(i, j) for i in range(self.rows) for j in range(self.cols)]
        positions.remove((row, col))
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor_pos = (row + dx, col + dy)
                if neighbor_pos in positions:
                    positions.remove(neighbor_pos)

        self.mine_positions = random.sample(positions, mines)
        for pos in self.mine_positions:
            x, y = pos
            self.minefield[x][y] = -1
            self.minefield_shadow[x][y] = -1

        for row in range(self.rows):
            for col in range(self.cols):
                if self.minefield[row][col] != -1:
                    count = 0
                    for r in [-1, 0, 1]:
                        for c in [-1, 0, 1]:
                            if (0 <= row + r < self.rows) and (0 <= col + c < self.cols) \
                                    and self.minefield[row + r][col + c] == -1:
                                c += 1
                                count += 1
                    self.minefield_shadow[row][col] = count



    def reveal_cells(self, row, col):
        button = self.buttons[row][col]
        val = self.minefield_shadow[row][col]
        if val == -1:
            button.setIcon(QIcon('icons/mine.png'))
            button.setStyleSheet('QPushButton {background-color: #8296B4;}')
            return
        elif val == 0:
            button.setStyleSheet('QPushButton:disabled {background-color: #8296B4; color: black;}')
            button.setEnabled(False)
        else:
            button.setText(str(val))
            color = {
                1: "#0000FF",
                2: "#00FF00",
                3: "#FFFF00",
                4: "#FF7F00",
                5: "#FF0000",
                6: "#2E2B5F",
                7: "#8B00FF",
                8: "black"
            }.get(val)
            button.setStyleSheet(f'QPushButton:disabled {{background-color: #8296B4; color: {color};}}')
            button.setEnabled(False)
        self.cells_remain -= 1

    def cell_clicked(self, row, col):
        if self.first:
            self.place_mines(self.mines, row, col)
            self.first = False
            self.start_timer()
        if self.minefield[row][col] == -1:
            self.stop_timer()
            self.reveal_cells(row, col)
            self.game_over()
            self.buttons[row][col].setStyleSheet('Background-color: red')
            return
        else:
            self.flood_fill(row, col)
            if self.cells_remain == 0:
                self.game_win()

    def flood_fill(self, row, col):
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols:
            return
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        if self.minefield[row][col] != 0 or (self.revealed[row][col] == CellState.VISITED):
            return
        butt = self.buttons[row][col]
        self.revealed[row][col] = CellState.VISITED
        if not butt.icon().isNull():
            self.mines_left += 1
            butt.setIcon(QIcon())
        adj_mines = self.minefield_shadow[row][col]
        if adj_mines > 0:
            self.reveal_cells(row, col)
            return
        self.reveal_cells(row, col)
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            self.flood_fill(new_row, new_col)

    def try_again(self):
        self.try_again_btn.setIcon(self.standart_ico)
        self.minefield = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.minefield_shadow = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[CellState.UNVISITED for _ in range(self.cols)] for _ in range(self.rows)]
        self.cells_remain = self.rows * self.cols - self.mines
        self.mine_positions = None
        self.first = True
        self.timer_off = True
        self.stop_timer()
        self.game_is_over = False
        self.mines_left = self.mines
        self.update_mines_left_lcd()
        self.timer_lcd.display(0)
        self.create_game_board(refresh=True)

    def game_over(self):
        self.try_again_btn.setIcon(self.lose_ico)
        self.game_is_over = True
        for x, y in self.mine_positions:
            self.reveal_cells(x, y)

    def game_win(self):
        self.stop_timer()
        self.try_again_btn.setIcon(self.win_ico)
        add_result(self.user.id, SCORES.get(self.level))
