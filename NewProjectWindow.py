from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QScrollArea, QLineEdit, QWidget, QMessageBox,
    QFileDialog, QGridLayout
)
from Motors import MotorSetupWindow
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from datetime import datetime
import json
import os

# Class representing the New Project window

class NewProjectWindow(QMainWindow):
    closed = Signal() # Signal emitted when the window is closed

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_motordialogs()
        self.setWindowIcon(QIcon("graph/icon.png"))
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(
            Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint
        )
        self.setFixedSize(self.size())
        self.setMinimumSize(610, 300)
        self.setMaximumSize(610, 300)  
        self.setWindowTitle("Create new project")

    def clear_window(self): # Clear the motor widgets and remove them from the layout
        self.column = 0
        self.row = 0
        self.motor_widgets.clear()
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, MotorSetupWindow):
                widget.deleteLater()

    def edit_file(self): # Open a file dialog to edit an existing project file
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open file", "Projects", "Text files (*.json);;All files (*)", options=options
        )

        if file_name:
            try:
                with open(file_name, 'r') as file:
                    file_content = file.read()

                    file_content = json.loads(file_content)

                self.spinbox_changed_by_user = False
                max_Branch = max(int(item['branch']) for item in file_content)
                max_Motor = max(int(item['StepperNumber']) for item in file_content)
                self.Branches_SpinBox.setValue(max_Branch)
                self.Motors_SpinBox.setValue(max_Motor)
                self.clear_window()

                for element in file_content:
                    if element["function"]== "Rotation":
                        motor_widget = MotorSetupWindow(
                            self.AmountofBranches,
                            str(element['StepperNumber']),
                            str(element['branch']),
                            str(element['StepsPerRevolution']),
                            "",
                            str(element["function"]),
                            str(element["rotationDirection"]),
                            self.window
                        )
                    else:
                        motor_widget = MotorSetupWindow(
                            self.AmountofBranches,
                            str(element['StepperNumber']),
                            str(element['branch']),
                            "",
                            str(element["serial_no"]),
                            str(element["function"]),
                            self.window
                        )
                    self.motor_widgets.append(motor_widget)
                    motor_widget.setFixedSize(230, 230)

                    self.grid_layout.addWidget(motor_widget, self.row, self.column)
                    self.column += 1
                    if self.column == 2:
                        self.column = 0
                        self.row += 1
                    self.motor_widgets.append(motor_widget)

            except Exception as e:
                self.Error_box()
                
    def Error_box(self): # Display an error message in a message box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('The selected file is invalid')
        msg.setWindowTitle("Error")
        msg.exec_()

    def generate_txt(self):  # Generate a JSON project file based on the entered motor setups
        project_name = self.Project_Name.text()
        if project_name == "":
            project_name = str(datetime.now().strftime("%Y-%m-%d_%H-%M"))

        self.path = f'Projects\\{project_name}.json'
        
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        motors_list = []
        with open(self.path, 'w') as f:
            for motor_widget in self.motor_widgets:
                motors_list.append(motor_widget.get_values())
            f.write(json.dumps(motors_list, indent=2))

        self.closed.emit()
        self.close()

    def update_amount_of_branches(self): # Update the branches in the motor setup widgets based on the spin box value
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, MotorSetupWindow):
                widget.refresh_branches(self.Branches_SpinBox.value())
                
        if self.AmountofBranches> self.Branches_SpinBox.value():
            self.AmountofBranches=self.Branches_SpinBox.value()
        else:
            self.AmountofBranches=self.Branches_SpinBox.value()

        

    def update_motor_setup(self): # Update the motor setup based on the spin box value
        if self.AmountofMotors> self.Motors_SpinBox.value():
            new_height = 530 if self.Motors_SpinBox.value() > 2 else 300
            self.setMaximumHeight(new_height)
            self.setMinimumHeight(new_height)
            self.resize(610, new_height)
            self.move(self.x(), self.y())

            for motor in range (1, self.AmountofMotors + 1 - self.Motors_SpinBox.value()):
                self.motor_widgets.pop()
                self.column-=1
                if self.column<0:
                    self.column=1
                    self.row-=1
                widget = self.grid_layout.itemAt(self.grid_layout.count()-motor).widget()
                if isinstance(widget, MotorSetupWindow):
                    widget.deleteLater()
        else:
            new_height = 530 if self.Motors_SpinBox.value() > 2 else 300
            self.setMaximumHeight(new_height)
            self.setMinimumHeight(new_height)
            self.resize(610, new_height)
            self.move(self.x(), self.y())

            for motor in range (1, self.Motors_SpinBox.value() + 1 - self.AmountofMotors):
                widget= MotorSetupWindow(
                    self.AmountofBranches, str(self.AmountofMotors+motor), "", "", "", "", "", self.window
                )
                widget.setFixedSize(230, 230)

                self.grid_layout.addWidget(widget, self.row, self.column)
                self.column += 1
                if self.column ==2:
                    self.column=0
                    self.row +=1
                self.motor_widgets.append(widget)         
                
        self.AmountofMotors= self.Motors_SpinBox.value()
        self.spinbox_changed_by_user=True

    def init_motordialogs(self):

        self.layout = QVBoxLayout()
        self.amountslayout = QHBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.window = QWidget()
        scroll_area.setWidget(self.window)

        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.setCentralWidget(scroll_area)
        self.window.setLayout(self.layout)

        self.Branches_Label = QLabel("Amount of Branches: ")
        self.OpenProject_Button = QPushButton("Edit project...")
        self.Branches_SpinBox = QSpinBox()
        self.Branches_SpinBox.setMinimum(1)

        self.amountslayout.addWidget(self.Branches_Label)
        self.amountslayout.addWidget(self.Branches_SpinBox)


        self.Motors_Label = QLabel("Amount of Motors: ")

        self.Motors_SpinBox = QSpinBox()
        self.Motors_SpinBox.setMinimum(1)

        self.amountslayout.addWidget(self.Motors_Label)
        self.amountslayout.addWidget(self.Motors_SpinBox)


        self.amountslayout.addWidget(self.OpenProject_Button)

        self.AmountofBranches = int(self.Branches_SpinBox.text())
        self.AmountofMotors = int(self.Motors_SpinBox.text())

        self.layout.addLayout(self.amountslayout)
        self.path = ""
        self.motor_widgets = []

        self.Save_Layout = QHBoxLayout()
        self.Project_Name = QLineEdit()
        self.Project_Name.setPlaceholderText("Project File Name")
        self.Save_Layout.addWidget(self.Project_Name)


        self.Save_Button = QPushButton("Save Project")

        self.Save_Button = QPushButton()
        self.Save_Button.setText("Save Project")

        self.Save_Layout.addWidget(self.Save_Button)

        self.layout.addLayout(self.Save_Layout)

        self.grid_layout= QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.row=0
        self.column=0

        for index in range(self.AmountofMotors):
            MotorIndex = str(index + 1)
            motor_widget = MotorSetupWindow(
                self.AmountofBranches, MotorIndex, "", "", "", "", "", self.window
            )
            self.grid_layout.addWidget(motor_widget)
            self.motor_widgets.append(motor_widget)
            motor_widget.setFixedSize(230, 230)
            self.grid_layout.addWidget(motor_widget, self.row, self.column)
            self.column += 1
            if self.column ==2:
                self.column=0
                self.row +=1

        self.OpenProject_Button.clicked.connect(self.edit_file)
        self.Save_Button.clicked.connect(self.generate_txt)
        self.Branches_SpinBox.valueChanged.connect(self.update_amount_of_branches)
        self.Motors_SpinBox.valueChanged.connect(self.update_motor_setup)