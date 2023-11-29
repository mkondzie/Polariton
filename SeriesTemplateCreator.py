from PySide6.QtGui import QIntValidator, QColor, QIcon
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QPushButton, QLineEdit, QScrollArea
from CreateSemiTransparent import create_semi_transparent_image
import os
from datetime import datetime

class SeriesCreator(QDialog):
    custom_color = QColor(0, 179, 148)
    closed = Signal()

    def __init__(self, key):
        super().__init__()
        self.setWindowIcon(QIcon("graph/icon.png"))
        self.main_layout= QVBoxLayout()
        self.Polariton_Bar_Label = QLabel()
        container = QWidget()
        container.setFixedSize(600,40)
        self.y_geometry = 180
        self.setFixedSize(600,self.y_geometry)
        self.sequence_info_layout= QHBoxLayout()
        self.sequence_info_layout.setContentsMargins(0,0,20,0)
        self.bar_pixmap = create_semi_transparent_image("graph/Polariton.png", 1)
        scaled_pixmap = self.bar_pixmap.scaled(80, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.polaritonlayout= QHBoxLayout()
        self.Polariton_Bar_Label.setPixmap(scaled_pixmap)
        self.polaritonlayout.setAlignment(Qt.AlignLeft)

        self.sequence_labellayout= QHBoxLayout()
        self.sequence_labellayout.setContentsMargins(0,0,10,0)
        self.sequence_label = QLabel(f"Sequence creator for project #{key}")
        self.sequence_label.setStyleSheet("color: rgba(0, 0, 0, 75);")
        self.sequence_labellayout.setAlignment(Qt.AlignRight)
        self.polaritonlayout.addWidget(self.Polariton_Bar_Label)
        self.sequence_labellayout.addWidget(self.sequence_label)
        self.sequence_info_layout.addLayout(self.polaritonlayout)
        self.sequence_info_layout.addLayout(self.sequence_labellayout)

        self.buttonLayout= QHBoxLayout()
        self.leftbuttonlayout = QHBoxLayout()
        self.leftbuttonlayout.setAlignment(Qt.AlignLeft)

        self.rightbuttonlayout = QHBoxLayout()
        self.rightbuttonlayout.setAlignment(Qt.AlignRight)

        self.buttonLayout.addLayout(self.leftbuttonlayout)
        self.buttonLayout.addLayout(self.rightbuttonlayout)

        self.Add_Button = QPushButton("Add Action")
        self.Add_Button.setFixedSize(105, 35)
        self.Add_Button.setIcon(QIcon("graph/plus.png"))
        self.Add_Button.clicked.connect(self.add_new_actions)
        self.leftbuttonlayout.addWidget(self.Add_Button)

        self.Delete_Button = QPushButton("Remove Action")
        self.Delete_Button.setFixedSize(105, 35)
        self.Delete_Button.clicked.connect(self.delete_actions)
        self.Delete_Button.setIcon(QIcon("graph/remove.png"))
        self.leftbuttonlayout.addWidget(self.Delete_Button)

        self.Template_Name = QLineEdit()
        self.Template_Name.setPlaceholderText("Series Name")
        self.rightbuttonlayout.addWidget(self.Template_Name)
        self.Template_Name.setFixedSize(100, 35)

        self.SaveRun_Button = QPushButton("Save and Run")
        self.SaveRun_Button.setFixedSize(150, 35)
        self.SaveRun_Button.setIcon(QIcon("graph/saverun.png"))
        self.SaveRun_Button.clicked.connect(self.save_and_run)
        self.rightbuttonlayout.addWidget(self.SaveRun_Button)
        

        container.setLayout(self.sequence_info_layout)
        self.main_layout.addWidget(container)
        self.main_layout.addLayout(self.buttonLayout)
        self.setLayout(self.main_layout)

        self.engines=[]
        motor=''
        for letter in key:
            if letter != "P" and letter != "R":
                motor += letter
            else:
                if motor !='':
                    self.engines.append(motor)
                motor=''
                motor += letter
        self.engines.append(motor)

        print(self.engines)

        self.action_layout = QHBoxLayout()
        self.actions_layouts = []

        for name in self.engines:
            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignTop)
            layout.setAlignment(Qt.AlignCenter)
            self.actions_layouts.append(layout)
            label = QLabel(str(name))
            label.setAlignment(Qt.AlignCenter)
            label.setAlignment(Qt.AlignCenter)
            edit = QLineEdit()
            edit.setPlaceholderText("0")
            layout.addWidget(label)
            layout.addWidget(edit)
            self.action_layout.addLayout(layout)

        self.sequence_count = 1

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        label = QLabel('Repeat')
        label.setAlignment(Qt.AlignCenter)
        edit = QLineEdit()
        edit.setPlaceholderText("0")
        layout.addWidget(label)
        layout.addWidget(edit)
        self.action_layout.addLayout(layout)
        self.actions_layouts.append(layout)
       
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        scroll_layout.addLayout(self.action_layout)
        
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidget(scroll_widget)
        self.main_layout.addWidget(scroll_area)


    def add_new_actions(self):
        for layout in self.actions_layouts:
            edit = QLineEdit()
            edit.setPlaceholderText("0")
            layout.addWidget(edit)

        self.sequence_count += 1
        if self.y_geometry < 340:
            self.y_geometry += 25
            self.setFixedSize(600,self.y_geometry)


    def delete_actions(self):
        if self.sequence_count != 1:
            for layout in self.actions_layouts:
                widget = layout.itemAt(layout.count()-1).widget()
                if isinstance(widget, QLineEdit):
                        widget.deleteLater()
            self.sequence_count -= 1
        
        if self.y_geometry > 180:
            self.y_geometry -= 25
            self.setFixedSize(600,self.y_geometry)

    def save_and_run(self):
        Template_name = self.Template_Name.text()
        if Template_name == "":
            Template_name = str(datetime.now().strftime("%Y-%m-%d_%H-%M"))

        self.path = f'Templates\\{Template_name}.csv'

        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        
        with open(self.path, 'w', newline="\n") as writer:
            values = ""

            for engine in self.engines:
                values += ","
                values += engine

            values += "\n"
            writer.write(values[1:])

            for index in range (self.sequence_count):
                values = ""
                for layout in self.actions_layouts:
                    widget = layout.itemAt(1 + index).widget()
                    if isinstance(widget, QLineEdit):
                        values += ","
                        if widget.text() != "":
                            values += widget.text()
                        else:
                            values += '0'

                values += "\n"
                writer.write(values[1:])

        self.closed.emit()
        self.close()
