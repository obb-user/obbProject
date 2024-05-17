from PyQt6.QtWidgets import QApplication
import sys
from launcher.check_upd import UpdateCheckWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    update_check_window = UpdateCheckWindow()
    update_check_window.show()
    sys.exit(app.exec())
