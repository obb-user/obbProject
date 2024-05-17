from PyQt6.QtCore import QThread, pyqtSignal
from launcher.main_window.controller import BotController
from bot.bot_code import start_bot

class BotWorker(QThread):
    bot_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = BotController()

    def run(self):
        while self.controller.is_running:
            start_bot()
        self.bot_finished.emit()
