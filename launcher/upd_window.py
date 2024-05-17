from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QDesktopServices

from launcher.config import github_repo_url


class UpdWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("")
        self.setFixedSize(300, 200)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Убираем рамку

        # Создание кнопки закрытия окна
        self.close_button = QPushButton("✕", self)
        self.close_button.setStyleSheet("background-color: red; color: white; border: none;")
        self.close_button.setGeometry(270, 0, 30, 30)
        self.close_button.clicked.connect(self.close)

        # Создание кнопки сворачивания окна
        self.minimize_button = QPushButton("−", self)
        self.minimize_button.setStyleSheet("background-color: blue; color: white; border: none;")
        self.minimize_button.setGeometry(240, 0, 30, 30)
        self.minimize_button.clicked.connect(self.showMinimized)

        # Создание текста по середине окна
        self.text_label = QLabel("Эта версия бота устарела. Пожалуйста, обновитесь.", self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setGeometry(0, 70, 300, 50)

        # Создание кнопки скачивания
        self.download_button = QPushButton("Скачать", self)
        self.download_button.setGeometry(100, 140, 100, 30)
        self.download_button.clicked.connect(self.download_update)

    def download_update(self):
        # Действие по скачиванию обновления
        # Например, открытие ссылки в браузере
        QDesktopServices.openUrl(QUrl(f"{github_repo_url}/releases/latest"))

