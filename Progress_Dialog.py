from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

# Creates progress dialog widget
class ProgresssDialog(QtWidgets.QDialog):
    def __init__(self, title, label):
        super().__init__()

        self.setWindowTitle(title)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon("graph/icon.png"))
        self.setModal(True)
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setFixedSize(300,75)
        self.label = QLabel(label)
        layout.addWidget(self.label)
        self.setLayout(layout)
        