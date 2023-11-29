from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIntValidator, QColor, QPixmap, QIcon
from PySide6.QtWidgets import QLabel, QSpinBox, QPushButton, QMessageBox
from Position_Controler import Config_Engines, Homing, Move_to_Position, Close_Connection
from CommandCenter import commandMove
import numpy as np

# Function to display an error window with the given message

def show_error_window(msg):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("Error")
        msg_box.setInformativeText(msg)
        msg_box.setWindowTitle("Error")
        msg_box.resize(150, 50)
        msg_box.exec()

# Class for the widget to control position in relative mode
class RelativeRotationControlWidget(QtWidgets.QWidget):
    custom_color = QColor(0, 179, 148)

    def __init__(self, branch, function, element):
        super().__init__()
        self.motor= element
        self.create_motor_layout(branch, function)

    def create_motor_layout(self, branch, function):
        layout = QtWidgets.QVBoxLayout()

        motor_group_box = QtWidgets.QGroupBox(f"{function.capitalize()} motor in branch {branch}")
        motor_layout = QtWidgets.QVBoxLayout(motor_group_box)

        actual_position_layout = QtWidgets.QHBoxLayout()
        actual_position_label = QLabel("Actual angle:")
        self.actual_position_display = QLabel(str(self.motor.angle) + "°")
        self.actual_position_display.setMaximumSize(100, 20)
        actual_position_layout.addWidget(actual_position_label)
        actual_position_layout.addWidget(self.actual_position_display)

        self.move_layout = QtWidgets.QHBoxLayout()
        self.move_forward_button = QPushButton()
        self.move_forward_button.setIcon(QIcon("graph/Move_Forward.png"))

        self.move_value_spinbox= QSpinBox()
        self.move_value_spinbox.setMinimum(0)
        self.move_value_spinbox.setMaximum(180)
        self.move_value_spinbox.setSingleStep(5)

        self.move_backward_button = QPushButton()
        self.move_backward_button.setIcon(QIcon("graph/Move_Backward.png"))
    
        self.move_layout.addWidget(self.move_backward_button)
        self.move_layout.addWidget(self.move_value_spinbox)
        self.move_layout.addWidget(self.move_forward_button)

        motor_layout.addLayout(actual_position_layout)
        motor_layout.addLayout(self.move_layout)
        layout.addWidget(motor_group_box)
        self.setLayout(layout)

        self.move_value_spinbox.editingFinished.connect(self.textchanged)
        self.move_forward_button.clicked.connect(self.rotate_forward)
        self.move_backward_button.clicked.connect(self.rotate_backward)

    def textchanged(self):
        text = self.move_value_spinbox.value()
        if text != "":
            value = int(text)
            rounded_value = round(value / 5) * 5 
            self.move_value_spinbox.setValue(rounded_value)

    def rotate_forward(self):
        commandMove(self.motor, self.move_value_spinbox.value())
        self.actual_position_display.setText(str(self.motor.angle) + "°")
    
    def rotate_backward(self):
        commandMove(self.motor, np.negative(self.move_value_spinbox.value()))
        self.actual_position_display.setText(str(self.motor.angle) + "°")
            
# Class for the widget to control position in relative mode
class RelativePositionControlWidget(QtWidgets.QWidget):
    custom_color = QColor(0, 179, 148)

    def __init__(self, branch, function, element):
        super().__init__()
        self.motor= element
        self.create_motor_layout(branch, function)

    def create_motor_layout(self, branch, function):
        layout = QtWidgets.QVBoxLayout()

        motor_group_box = QtWidgets.QGroupBox(f"{function.capitalize()} motor in branch {branch}")
        motor_layout = QtWidgets.QVBoxLayout(motor_group_box)
        actual_position_layout = QtWidgets.QHBoxLayout()

        actual_position_label = QLabel("Actual delay:")
        self.actual_position_display = QLabel(str(self.motor.position)+ " ps")
        self.actual_position_display.setMaximumSize(100, 20)
        actual_position_layout.addWidget(actual_position_label)
        actual_position_layout.addWidget(self.actual_position_display)

        
        self.move_layout = QtWidgets.QHBoxLayout()
        self.move_forward_button = QPushButton()
        self.move_forward_button.setIcon(QIcon("graph/Move_Forward.png"))

        self.move_value_spinbox= QSpinBox()
        self.move_value_spinbox.setMinimum(0)
        self.move_value_spinbox.setMaximum(160)
        self.move_value_spinbox.setSingleStep(5)

        self.move_backward_button = QPushButton()
        self.move_backward_button.setIcon(QIcon("graph/Move_Backward.png"))
    
        self.move_layout.addWidget(self.move_backward_button)
        self.move_layout.addWidget(self.move_value_spinbox)
        self.move_layout.addWidget(self.move_forward_button)

        motor_layout.addLayout(actual_position_layout)
        motor_layout.addLayout(self.move_layout)
        layout.addWidget(motor_group_box)
        self.setLayout(layout)

        self.move_value_spinbox.editingFinished.connect(self.textchanged)
        self.move_forward_button.clicked.connect(self.move_forward)
        self.move_backward_button.clicked.connect(self.move_backward)

    def textchanged(self):
        text = self.move_value_spinbox.value()

        if text != "":
            value = int(text)
            rounded_value = round(value / 5) * 5 
            self.move_value_spinbox.setValue(rounded_value)
    
    def move_forward(self):
        if (self.motor.position + self.move_value_spinbox.value() > 320):
            show_error_window("The selected value is too large")
        else:
            self.motor.position = int(self.motor.position + self.move_value_spinbox.value())
            Move_to_Position(self.motor.index, self.motor.position)
            self.actual_position_display.setText(str(self.motor.position) + "ps")
    
    def move_backward(self):
        if (self.motor.position - self.move_value_spinbox.value() < 0):
            show_error_window("The selected value is too small")
        else:    
            self.motor.position = int(self.motor.position - self.move_value_spinbox.value())
            Move_to_Position(self.motor.index, self.motor.position)
            self.actual_position_display.setText(str(self.motor.position) + "ps")
    


