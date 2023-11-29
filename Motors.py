from PySide6.QtWidgets import (
    QLineEdit, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QRadioButton, QFrame
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt

import serial.tools.list_ports

# Class representing a rotation motor

class Rotation_Motor:
    all = []

    def __init__(self, com, pins, branch, function, steps_per_revolution=64, angle=0, number=None, velocity=400, direction='Right'):
        self.com = com  # Port, np. COM3
        self.pins = pins  # Piny na plytce Arduino, np. [8,9,10,11]
        self.branch = branch  # Gałąź układu pomiarowego
        self.function = function  # Obracanie albo przesuwanie na prowadnicy
        self.number = number  # Numer unikatowo identyfikujący silnik
        self.steps_per_revolution = steps_per_revolution
        self.velocity = velocity
        self.angle = angle  # aktualna pozycja silnka. domyślnie zero. zmiania sie z obrotem silnika
        self.index = int(self.com in [m.com for m in
                                   Rotation_Motor.all])  # do identyfikacji na płytce Arduino. Może być 1 albo 2
        Rotation_Motor.all.append(self)
        self.direction= direction

    def rotate(self, angle):  # zapisuje o ile obrócił sie siknik
        self.angle += angle
        self.angle %=360

    def clear_self(self):
        Rotation_Motor.all.remove(self)

# Class representing a position motor

class Position_Motor:
    all=[]
    def __init__(self, branch, function, index, position=0, serial_no="28251515", number=None):
        self.branch = branch
        self.function = function
        self.number = number
        self.serial_no= serial_no
        self.position = position
        self.index = index
        Position_Motor.all.append(self)

    def move(self, position):
        self.position += position

# Class representing the motor setup widegt

class MotorSetupWindow(QWidget):
    def __init__(self, AmountofBranches, MotorIndex, Branch="", Steps="", serial_no="", Func="", rotationDirection="", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AmountofBranches = AmountofBranches
        self.Available_Ports = serial.tools.list_ports.comports()
        self.Motor_Index = MotorIndex
        self.Main_Layout = QVBoxLayout()
        self.setLayout(self.Main_Layout)

        self.frame_container = QFrame(self)
        self.frame_container.setFrameShape(QFrame.Panel)
        self.frame_container.setFrameShadow(QFrame.Sunken)
        self.frame_layout = QVBoxLayout(self.frame_container)

        self.Motor_name = QLabel()
        self.Motor_name.setObjectName("Motor_name")
        self.Motor_name.setText("Motor " + self.Motor_Index)
        self.Motor_name.setAlignment(Qt.AlignCenter)
        self.frame_layout.addWidget(self.Motor_name)

        self.Branch_Label = QLabel("Branch: ")
        self.Branch_Label.setObjectName("Branch_Label")
        self.frame_layout.addWidget(self.Branch_Label)

        self.Branch_box = QComboBox()
        self.Branch_box.setObjectName("Branch_box")

        self.frame_layout.addWidget(self.Branch_box)

        for num in range(self.AmountofBranches):
            self.Branch_box.addItem(str(num + 1))

        self.frame_layout.addWidget(self.Branch_box)

        if Branch != "":
            self.Branch_box.setCurrentIndex(int(Branch) - 1)

        self.BranchesLayout = QHBoxLayout()
        self.BranchesLayout.setObjectName("BranchesLayout")
        self.BranchesLayout.addWidget(self.Branch_Label)
        self.BranchesLayout.addWidget(self.Branch_box)

        self.Com_label = QLabel("COM: ")
        self.Com_label.setObjectName("Com_label")

        self.com_box = QComboBox()
        self.com_box.setObjectName("com_box")

        for element in self.Available_Ports:
            self.com_box.addItem(str(element.device))

        self.COMLayout = QHBoxLayout()
        self.COMLayout.setObjectName("COMLayout")
        self.COMLayout.addWidget(self.Com_label)
        self.COMLayout.addWidget(self.com_box)

        self.Rotation = QRadioButton("Rotation")
        self.Rotation.setObjectName("Rotation")

        self.Position = QRadioButton("Position")
        self.Position.setObjectName("Position")

        if Func == "Rotation" or Func == "":
            self.Position.setChecked(False)
            self.Rotation.setChecked(True)
        else:
            self.Rotation.setChecked(False)
            self.Position.setChecked(True)

        self.RotPosLayout = QHBoxLayout()
        self.RotPosLayout.setObjectName("RotPosLayout")
        self.RotPosLayout.addWidget(self.Rotation, alignment=Qt.AlignCenter)
        self.RotPosLayout.addWidget(self.Position, alignment=Qt.AlignCenter)

        self.frame_layout.addWidget(self.Motor_name)
        self.frame_layout.addLayout(self.RotPosLayout)
        self.frame_layout.addLayout(self.BranchesLayout)
        self.frame_layout.addLayout(self.COMLayout)

        self.draw_rotation_layout(Steps, rotationDirection)
        self.draw_position_layout(serial_no)

        self.Rotation.toggled.connect(self.show_rotation_layout)
        self.Position.toggled.connect(self.show_position_layout)

        self.Main_Layout.addWidget(self.frame_container)

        if(self.Position.isChecked()):
            self.show_position_layout()
        else:
            self.show_rotation_layout()

    def draw_rotation_layout(self, Steps, direction):
        self.PINSLayout = QHBoxLayout()
        self.PINSLayout.setObjectName("PINSLayout")

        self.Pins_label = QLabel("Pins: ")
        self.Pins_label.setObjectName("Pins_label")
        self.PINSLayout.addWidget(self.Pins_label)

        self.pins = [QSpinBox() for _ in range(4)]

        for element in self.pins:
            element.setMinimum(1)
            element.setMaximum(54)
            self.PINSLayout.addWidget(element)

        self.RevolutionLayout = QHBoxLayout()
        self.RevolutionLayout.setObjectName("RevLay")

        self.Revolution_Label = QLabel("Steps per revfolution:")
        self.Revolution_Line = QLineEdit()
        self.Revolution_Line.setPlaceholderText("64")
        self.Revolution_Line.setValidator(QIntValidator())

        self.Direction_Layout = QHBoxLayout()
        self.Direction_Layout.setObjectName("Direct")

        if Steps != "":
            self.Revolution_Line.setText(Steps)

        self.RevolutionLayout.addWidget(self.Revolution_Label)
        self.RevolutionLayout.addWidget(self.Revolution_Line)

        self.Diretcion_Label = QLabel("Rotation direction:")
        self.Direction_box = QComboBox()
        self.Direction_box.addItem("Right")
        self.Direction_box.addItem("Left")

        if direction != "":
            self.Direction_box.setCurrentText(str(direction))
            
        self.Direction_Layout.addWidget(self.Diretcion_Label)
        self.Direction_Layout.addWidget(self.Direction_box)

        self.frame_layout.addLayout(self.PINSLayout)
        self.frame_layout.addLayout(self.Direction_Layout)
        self.frame_layout.addLayout(self.RevolutionLayout)

    def draw_position_layout(self, serial_no):
        self.Serial_Layout = QHBoxLayout()
        self.Serial_Layout.setObjectName("Serial_Layout")

        self.Serial_Label = QLabel("Serial Number:")
        self.Serial_Line = QLineEdit()
        self.Serial_Line.setPlaceholderText("28251515")
        self.Serial_Line.setValidator(QIntValidator())

        if serial_no != "":
            self.Serial_Line.setText(serial_no)

        self.Serial_Layout.addWidget(self.Serial_Label)
        self.Serial_Layout.addWidget(self.Serial_Line)

        self.frame_layout.addLayout(self.Serial_Layout)

    def show_position_layout(self):
        self.Pins_label.hide()
        for pin in self.pins:
            pin.hide()
        self.Com_label.hide()
        self.com_box.hide()
        self.Revolution_Label.hide()
        self.Revolution_Line.hide()
        self.Direction_box.hide()
        self.Diretcion_Label.hide()
        self.Serial_Label.show()
        self.Serial_Line.show()

    def show_rotation_layout(self):
        self.Pins_label.show()
        for pin in self.pins:
            pin.show()
        self.Com_label.show()
        self.com_box.show()
        self.Revolution_Label.show()
        self.Revolution_Line.show()
        self.Serial_Label.hide()
        self.Serial_Line.hide()
        self.Direction_box.show()
        self.Diretcion_Label.show()

    def refresh_branches(self, amountofBranches):
        
        if self.AmountofBranches > amountofBranches:
            for branch in range (amountofBranches, self.AmountofBranches):
                self.Branch_box.removeItem(amountofBranches)

            self.AmountofBranches= amountofBranches
        else:
            for branch in range (self.AmountofBranches, amountofBranches):
                self.Branch_box.addItem(str(branch+1))
        
            self.AmountofBranches= amountofBranches

    def get_values(self):
        motor_id = {}

        if self.Position.isChecked():
            motor_id['function'] = "Position"
            motor_id['StepperNumber'] = int(self.Motor_Index)
            motor_id['branch'] = self.Branch_box.currentText()
            if self.Serial_Line.text()=="":
                motor_id['serial_no'] = str(self.Serial_Line.placeholderText())
            else:
                motor_id['serial_no']= str(self.Serial_Line.text())

        else:
            motor_id['function'] = "Rotation"
            motor_id['StepperNumber'] = int(self.Motor_Index)
            motor_id['branch'] = self.Branch_box.currentText()
            motor_id['com'] = str(self.com_box.currentText())

            if self.Revolution_Line.text() == "":
                motor_id["StepsPerRevolution"] = int(self.Revolution_Line.placeholderText())
            else:
                motor_id["StepsPerRevolution"] = int(self.Revolution_Line.text())

            motor_id['pins'] = [int(p.text()) for p in self.pins]
            motor_id['rotationDirection']= self.Direction_box.currentText()
            
            motor_id["angle"] = 0
            motor_id["velocity"] = 400

        return motor_id
