import requests
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, QLabel
from launcher.main_window.main_window import MainWindow
from launcher.config import *
from launcher.upd_window.upd_window import UpdWindow


class UpdateCheckWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Проверка обновления")
        self.setFixedSize(300, 200)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Убираем рамку

        self.label = QLabel("Проверка обновления...", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, 100, 300, 30)

        self.main_window = None  # Инициализируем атрибут заранее

        # Выполняем запрос в другом методе
        self.check_for_updates()

    def check_for_updates(self):
        response = requests.get(f'{github_repo_url}/releases/latest', allow_redirects=False)

        if response.status_code == 302:  # Проверяем, что ответ - редирект
            latest_release_url = response.headers['Location']
            latest_version = latest_release_url.split('/')[-1]  # Получаем последний сегмент URL, содержащий версию
            if latest_version == client_version:
                QTimer.singleShot(0, self.open_main_window)
            else:
                QTimer.singleShot(0, self.open_upd_window)
        else:
            print("Ошибка: Не удалось получить данные. Статус код:", response.status_code)

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def open_upd_window(self):
        self.upd_window = UpdWindow()
        self.upd_window.show()
        self.close()

