import sys
from PySide6.QtWidgets import QApplication
from core.app import TEACH

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TEACH()
    window.show()
    sys.exit(app.exec())
