# main_window.py
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel
from launcher.main_window.worker import BotWorker
from launcher.config import client_version
import keyboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("")
        self.setFixedSize(300, 200)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Убираем рамку

        self.bot_worker = BotWorker()
        self.bot_worker.bot_finished.connect(self.bot_finished)

        # Создание кастомной рамки с названием
        self.title_bar = QLabel("Бот рыбалка", self)
        self.title_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_bar.setStyleSheet("background-color: lightgray")
        self.title_bar.setGeometry(0, 0, 300, 30)

        # Добавление текста
        self.left_label = QLabel("obb-team", self)
        self.left_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.left_label.setGeometry(10, 170, 100, 30)

        # Добавление версии приложения из конфига в правый верхний угол окна
        self.version_label = QLabel(client_version, self)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.version_label.setGeometry(200, 170, 90, 30)

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

        # Создание кнопки управления ботом
        self.bot_button = QPushButton("Запустить бота", self)
        self.bot_button.setGeometry(100, 100, 100, 50)
        self.bot_button.clicked.connect(self.toggle_bot_state)

        # Биндинг клавиш Ctrl+1 для управления ботом
        keyboard.add_hotkey('ctrl+1', self.toggle_bot_state)

    def toggle_bot_state(self):
        new_text = self.bot_worker.controller.toggle_bot_state()
        self.bot_button.setText(new_text)

        if self.bot_worker.controller.is_running:
            self.bot_worker.start()  # Если бот запущен, запускаем поток
        else:
            # Здесь можно добавить логику для остановки бота, если это необходимо
            pass

    def bot_finished(self):
        # Логика для остановки бота
        print("Бот остановлен.")

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.title_bar.geometry().contains(event.pos()):
            self.drag_start_position = event.globalPosition() - self.frameGeometry().topLeft().toPointF()
        else:
            self.drag_start_position = None

    def mouseMoveEvent(self, event):
        if self.drag_start_position:
            new_position = event.globalPosition() - self.drag_start_position
            self.move(new_position.toPoint())

    def mouseReleaseEvent(self, event):
        self.drag_start_position = None
