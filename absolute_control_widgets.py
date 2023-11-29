from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIntValidator, QColor
from PySide6.QtCore import Qt

# Class for the widget to control rotation in absolute mode

class AbsoluteRotationControlWidget(QtWidgets.QWidget):
    custom_color = QColor(0, 179, 148)

    def targetchange(self): 
        self.target_position_display.setText(str(self.position_slider.value()))

    def textchanged(self):
        if self.target_position_display.text() != "":
            self.position_slider.setValue(int(self.target_position_display.text()))
        else:
            self.target_position_display.setText(str(self.position_slider.value()))

    def create_motor_layout(self, branch, function):
        layout = QtWidgets.QVBoxLayout()
        onlyInt = QIntValidator(0, 360)

        motor_group_box = QtWidgets.QGroupBox(f"{function.capitalize()} motor in branch {branch}")
        motor_layout = QtWidgets.QVBoxLayout(motor_group_box)
        actual_position_layout = QtWidgets.QHBoxLayout()
        target_position_layout = QtWidgets.QHBoxLayout()

        actual_position_label = QtWidgets.QLabel("Actual angle:")
        self.actual_position_display = QtWidgets.QLabel(str(self.motor.angle)+ " °")
        self.actual_position_display.setMaximumSize(100, 20)
        actual_position_layout.addWidget(actual_position_label)
        actual_position_layout.addWidget(self.actual_position_display)

        target_position_label = QtWidgets.QLabel("Target angle:")
        self.target_position_display = QtWidgets.QLineEdit()
        self.target_position_display.setValidator(onlyInt)
        self.target_position_display.setText("0")
        target_position_layout.addWidget(target_position_label)
        target_position_layout.addWidget(self.target_position_display)

        self.position_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.position_slider.valueChanged.connect(self.targetchange)
        self.position_slider.setMaximum(360)
        self.position_slider.setMinimum(0)
        self.target_position_display.textChanged.connect(self.textchanged)
        self.position_slider.setStyleSheet(f"QSlider::handle:horizontal {{ background-color: {self.custom_color.name()}; }}")
        motor_layout.addLayout(actual_position_layout)
        motor_layout.addLayout(target_position_layout)
        motor_layout.addWidget(self.position_slider)
        layout.addWidget(motor_group_box)
        self.setLayout(layout)

    def __init__(self, branch, function, element):
        self.motor= element
        super().__init__()
        self.create_motor_layout(branch, function)

# Class for the widget to control position in absolute mode
class AbsolutePositionControlWidget(QtWidgets.QWidget):
    custom_color = QColor(0, 179, 148)

    def targetchange(self):
        self.target_position_display.setText(str(self.position_slider.value()))

    def textchanged(self):
        if self.target_position_display.text() != "":
            self.position_slider.setValue(int(self.target_position_display.text()))
        else:
            self.target_position_display.setText(str(self.position_slider.value()))

    def create_motor_layout(self, branch, function):
        layout = QtWidgets.QVBoxLayout()
        onlyInt = QIntValidator(0, 320)

        motor_group_box = QtWidgets.QGroupBox(f"{function.capitalize()} motor in branch {branch}")
        motor_layout = QtWidgets.QVBoxLayout(motor_group_box)
        actual_position_layout = QtWidgets.QHBoxLayout()
        target_position_layout = QtWidgets.QHBoxLayout()

        actual_position_label = QtWidgets.QLabel("Actual delay:")
        self.actual_position_display = QtWidgets.QLabel(str(self.motor.position)+ " ps")
        self.actual_position_display.setMaximumSize(100, 20)
        actual_position_layout.addWidget(actual_position_label)
        actual_position_layout.addWidget(self.actual_position_display)

        target_position_label = QtWidgets.QLabel("Target delay:")
        self.target_position_display = QtWidgets.QLineEdit()
        self.target_position_display.setValidator(onlyInt)
        self.target_position_display.setText("0")
        target_position_layout.addWidget(target_position_label)
        target_position_layout.addWidget(self.target_position_display)

        self.position_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.position_slider.valueChanged.connect(self.targetchange)
        self.position_slider.setMaximum(320)
        self.position_slider.setMinimum(0)
        self.target_position_display.textChanged.connect(self.textchanged)
        self.position_slider.setStyleSheet(f"QSlider::handle:horizontal {{ background-color: {self.custom_color.name()}; }}")
        motor_layout.addLayout(actual_position_layout)
        motor_layout.addLayout(target_position_layout)
        motor_layout.addWidget(self.position_slider)
        layout.addWidget(motor_group_box)
        self.setLayout(layout)

    def __init__(self, branch, function, element):
        self.motor= element
        super().__init__()
        self.create_motor_layout(branch, function)

