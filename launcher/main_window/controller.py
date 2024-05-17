class BotController:
    def __init__(self):
        self.is_running = False

    def toggle_bot_state(self):
        self.is_running = not self.is_running
        return "Остановить бота" if self.is_running else "Запустить бота"
