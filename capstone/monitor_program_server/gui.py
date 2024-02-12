from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QDateTime
import sys


class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log Window")
        self.setFixedSize(800, 600)  # 창의 고정 크기 설정

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("background-color: #f0f0f0; font-family: Arial;")

        self.button = QPushButton("Add Log")
        self.button.setStyleSheet("background-color: #4caf50; color: white;")
        self.button.clicked.connect(self.add_log)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_log(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        log_message = f"Log message at {current_time}"
        self.text_edit.append(log_message)


def start_gui():
    app = QApplication(sys.argv)
    window = LogWindow()
    window.show()
    sys.exit(app.exec_())


start_gui()
