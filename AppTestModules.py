import sys
from PySide6.QtWidgets import QApplication
from SeriesTemplateCreator import SeriesCreator

# Module to test new windows
if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = SeriesCreator("R1R2R3R4P1P2")

    win.show()

    sys.exit(app.exec())