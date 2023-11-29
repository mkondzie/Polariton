from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QIcon, QIntValidator
import serial.tools.list_ports

# Class for the setting dialog window

class SettingsDialog(QtWidgets.QDialog):
    controlModeChanged = QtCore.Signal(list)
    
    def __init__(self, mode, com, time=2):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setWindowIcon(QIcon("graph/icon.png"))
        layout = QtWidgets.QVBoxLayout()

        control_layout = QtWidgets.QHBoxLayout()

        control_label = QtWidgets.QLabel("Control Mode:")
        control_layout.addWidget(control_label)

        self.control_edit = QtWidgets.QComboBox()
        self.control_edit.addItem("Absolute")
        self.control_edit.addItem("Relative")
        control_layout.addWidget(self.control_edit)

        self.control_edit.setCurrentText(mode)
        layout.addLayout(control_layout)

        self.Com_label = QtWidgets.QLabel("Trigger com: ")
        self.Com_label.setObjectName("Com_label")

        self.com_box = QtWidgets.QComboBox()
        self.com_box.setObjectName("com_box")
        self.Available_Ports = serial.tools.list_ports.comports()

        for element in self.Available_Ports:
            self.com_box.addItem(str(element.device))

        self.com_box.setCurrentText(com)
        self.com_layout= QtWidgets.QHBoxLayout()
        self.com_layout.addWidget(self.Com_label)
        self.com_layout.addWidget(self.com_box)
        layout.addLayout(self.com_layout)

        self. time_layout = QtWidgets.QHBoxLayout()
        self.time_label = QtWidgets.QLabel("Mesaurement time: ")
        self.time_edit = QtWidgets.QLineEdit()
        self.time_edit.setValidator(QIntValidator())
        self.time_edit.setText(str(time))
        self.time_layout.addWidget(self.time_label)
        self.time_layout.addWidget(self.time_edit)

        layout.addLayout(self.time_layout)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_settings)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

    # Save the selected settings and emit the signal
    def save_settings(self):
        selected=[]
        selected_mode = self.control_edit.currentText()
        selected_com = self.com_box.currentText()
        selected_time = self.time_edit.text()
        selected.append(selected_mode)
        selected.append(selected_com)
        selected.append(selected_time)
        self.controlModeChanged.emit(selected)
        self.accept()