from PyQt6.QtCore import pyqtSignal, QRect, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QToolButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QPushButton
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


class ResultsWidget(QWidget):
    switch_to_main_page = pyqtSignal()

    def __init__(self, results):
        super().__init__()
        self.results = results
        self.setStyleSheet("background-color:#B0BFD7")
        title_label = QLabel("Players results:", parent=self)
        title_label.setGeometry(QRect(80, 10, 200, 30))
        font = QFont()
        font.setFamily("Copperplate Gothic Bold")
        font.setPointSize(16)
        title_label.setFont(font)
        title_label.setStyleSheet('Background-color: #8296B4 ')
        self.menu_btn = QToolButton(parent=self)
        self.menu_btn.setGeometry(QRect(10, 10, 31, 31))
        self.menu_btn.setFont(font)
        self.menu_btn.setAutoFillBackground(False)
        self.menu_btn.setStyleSheet("background-color:#B0BFD7\n")
        self.export_btn = QPushButton('Export to pdf', parent=self)
        self.export_btn.setGeometry(QRect(500, 10, 170, 30))
        self.export_btn.setFont(font)
        self.export_btn.setStyleSheet("background-color:#B0BFD7")
        self.export_btn.clicked.connect(self.export_to_pdf)
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/menu.svg"), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_btn.setIcon(icon)
        self.menu_btn.setIconSize(QSize(18, 18))
        self.menu_btn.clicked.connect(self.go_to_menu)
        self.table = QTableWidget(parent=self)
        self.table.setGeometry(QRect(35, 50, 650, 420))
        self.table.setFont(font)
        self.setStyleSheet('Background-color: #B0BFD7')
        self.table.setRowCount(len(results))
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 350)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(["Nicknames", "Scores"])
        font.setPointSize(11)
        self.table.horizontalHeader().setFont(font)
        self.table.horizontalHeader().setStyleSheet("QTableWidget disabled:{background-color:#B0BFD7}")
        self.table.horizontalHeader().setEnabled(False)
        self.table.verticalHeader().setEnabled(False)

        for row, result in enumerate(results):
            username, score = result.split(" - ")
            self.table.setItem(row, 0, QTableWidgetItem(username))
            self.table.setItem(row, 1, QTableWidgetItem(score))

        self.table.horizontalHeader().setStretchLastSection(True)
        self.setFixedSize(720, 480)
        self.setWindowTitle("Players results:")

    def update_results(self, new_results):
        self.table.clearContents()
        self.table.setRowCount(len(new_results))
        for row, result in enumerate(new_results):
            username, score = result.split(" - ")
            self.table.setItem(row, 0, QTableWidgetItem(username))
            self.table.setItem(row, 1, QTableWidgetItem(score))
        self.table.update()

    def go_to_menu(self):
        self.switch_to_main_page.emit()

    def export_to_pdf(self):
        pdf = canvas.Canvas("results.pdf", pagesize=letter)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(300, 750, "Results")
        pdf.setFont("Helvetica-Bold", 12)
        pdf.setFillColor(colors.gray)
        pdf.drawString(50, 700, "Username")
        pdf.drawString(200, 700, "Score")
        pdf.setFont("Helvetica", 12)
        pdf.setFillColor(colors.black)
        y = 680
        for result in self.results:
            res = result.split('-')
            username = res[0]
            score = res[1]
            pdf.drawString(50, y, username)
            pdf.drawString(200, y, str(score))
            y -= 20

        pdf.save()
