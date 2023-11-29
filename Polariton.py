from PySide6 import QtCore, QtWidgets
from NewProjectWindow import NewProjectWindow
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QPushButton, QScrollArea, QLabel, QHBoxLayout, QFrame, QSpacerItem
from PySide6.QtGui import QAction, QIcon, QPixmap, QColor, QPainter
import json
from Motors import Position_Motor, Rotation_Motor
from absolute_control_widgets import AbsoluteRotationControlWidget, AbsolutePositionControlWidget
from PySide6.QtCore import QThread, QObject, Qt
from SettingDialog import SettingsDialog
from CommandCenter import moveToAngle, InitMotorsFromList, initSerials, Process_Commands, commandTrigger
from time import sleep
from Progress_Dialog import ProgresssDialog
from CreateSemiTransparent import create_semi_transparent_image
from SeriesTemplateCreator import SeriesCreator

# The processor class is used to process commands in the background
class Processor(QObject): # Runs Process_Command every 100 ms
    def __init__(self):
        super().__init__()
        self.running = True

    def start(self):
        self.running = True
        self.run()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            Process_Commands()
            QThread.msleep(100)

# The main window interface class

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    # Method called when the window is closed
    def on_window_closed(self, event): # Sets the motors to position 0 when the application is closed
        if len(self.motors_list) !=0:
            self.reset_position()
            pass
        if len(self.position_motorlist) !=0:
            Close_Connection()
            pass

        if self.background_thread is not None:
            self.background_worker.stop()
            self.background_thread.quit()
            self.background_thread.wait()

        event.accept()

    # Initialize the main window interface
    def setupUi(self, MainWindow): #Create main window layout
        self.motors_list = []
        self.position_motorlist = []
        self.rotation_motorlist = []
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Polaritron")
        MainWindow.closeEvent = self.on_window_closed
        MainWindow.setWindowIcon(QIcon("graph/icon.png"))
        MainWindow.resize(1020, 600)
        MainWindow.setMaximumSize(1020, 600)
        MainWindow.setMinimumSize(1020, 600)
        self.background_thread= None
        self.control_mode= "Relative"
        self.trigger_com= "COM12"
        self.measurement_time = 2
        self.grid_layout = QtWidgets.QGridLayout()
        self.top_bar_layout = QHBoxLayout()
        self.top_bar_frame = QFrame()
        self.top_bar_layout.setContentsMargins(1,2,1,2)

        self.top_bar_frame.setFrameShape(QFrame.Box)
        self.top_bar_frame.setFrameShadow(QFrame.Sunken)
        self.top_bar_frame.setLineWidth(0)
        self.top_bar_frame.setMidLineWidth(1)
        self.top_bar_frame.setContentsMargins(0, 0, 0, 5)


        self.top_bar_frame.setLayout(self.top_bar_layout)

        self.buttons_Layout = QHBoxLayout()

        self.move_Layout = QHBoxLayout()
        self.move_Layout.setAlignment(QtCore.Qt.AlignRight)

        self.polariton_Layout = QHBoxLayout()
        self.polariton_Layout.setAlignment(QtCore.Qt.AlignLeft)

        self.buttons_Layout.addLayout(self.polariton_Layout)
        self.buttons_Layout.addLayout(self.move_Layout)

        self.Polariton_Bar_Label = QLabel()
        self.bar_pixmap = create_semi_transparent_image("graph/Polariton.png", 0.7)
        scaled_pixmap = self.bar_pixmap.scaled(105, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.Polariton_Bar_Label.setPixmap(scaled_pixmap)
        self.Polariton_Bar_Label.setVisible(False)
        self.polariton_Layout.addWidget(self.Polariton_Bar_Label)

        self.Mesure_Button = QPushButton("Mesure")
        self.Mesure_Button.clicked.connect(self.start_trigger)
        self.Mesure_Button.setFixedSize(105, 35)
        self.Mesure_Button.setIcon(QIcon("graph/Mesure.png"))
        self.move_Layout.addWidget(self.Mesure_Button)

        self.Move_Button = QPushButton("Move motors")
        self.Move_Button.clicked.connect(self.change_position)
        self.Move_Button.setFixedSize(105, 35)
        self.Move_Button.setIcon(QIcon("graph/play.png"))
        self.move_Layout.addWidget(self.Move_Button)

        self.Reset_button = QPushButton("Reset position")
        self.Reset_button.clicked.connect(self.reset_position)
        self.Reset_button.setFixedSize(105, 35)
        self.Reset_button.setIcon(QIcon("graph/reset.png"))
        self.move_Layout.addWidget(self.Reset_button)

        self.top_bar_frame.setVisible(False)
        
        self.Polariton_Label = QLabel()
        self.pixmap = create_semi_transparent_image("graph/Polariton.png", 0.2)
        self.Polariton_Label.setPixmap(self.pixmap)

        self.top_bar_layout.addLayout(self.buttons_Layout)

        vbox_layout = QtWidgets.QVBoxLayout()
        vbox_layout.addWidget(self.top_bar_frame)
        vbox_layout.setContentsMargins(0, 0, 0, 10)

        scroll_area = QScrollArea()
        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setWidgetResizable(True)
        scroll_layout.addLayout(self.grid_layout)
        scroll_layout.addWidget(self.Polariton_Label, alignment=QtCore.Qt.AlignCenter)
        scroll_area.setWidget(scroll_widget)
        vbox_layout.addWidget(scroll_area)
        vbox_layout.setStretch(1, 1)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLayout(vbox_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.actionConfig = QAction(MainWindow)
        self.actionConfig.setObjectName("actionConfig")
        self.actionConfig.setText("Config")
        self.actionConfig.triggered.connect(self.open_config_dialog)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menubar.setStyleSheet("background-color: rgba(235,235,235,250);"
                                   "border-bottom: 1px solid rgba(0, 0, 0, 0.5);")

        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuProject.setTitle("File")

        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuSettings.setTitle("Run")

        self.menuSettings_2 = QtWidgets.QMenu(self.menubar)
        self.menuSettings_2.setObjectName("menuSettings_2")
        self.menuSettings_2.setTitle("Settings")

        MainWindow.setMenuBar(self.menubar)

        self.actionNew_Project = QAction(MainWindow)
        self.actionNew_Project.setObjectName("actionNew_Project")
        self.actionNew_Project.setText("New Project")
        self.actionNew_Project.setShortcut("Ctrl+N")
        icon_newfile= QIcon()
        icon_newfile.addPixmap(QPixmap("graph/new.png")), QIcon.Mode.Normal
        self.actionNew_Project.setIcon(icon_newfile)
        self.actionNew_Project.triggered.connect(self.new_project)

        self.actionOpen_Project = QAction(MainWindow)
        self.actionOpen_Project.setObjectName("actionOpen_Project")
        self.actionOpen_Project.setText("Open Project")
        self.actionOpen_Project.setShortcut("Ctrl+O")

        icon_openfile= QIcon()
        icon_openfile.addPixmap(QPixmap("graph/open.png")), QIcon.Mode.Normal
        self.actionOpen_Project.setIcon(icon_openfile)
        self.actionOpen_Project.triggered.connect(self.open_project)

        self.actionNew_Series_Template = QAction(MainWindow)
        self.actionNew_Series_Template.setObjectName("actionNew_Series_Template")
        self.actionNew_Series_Template.setText("New Series Template")
        self.actionNew_Series_Template.setShortcut("F5")
        self.actionNew_Series_Template.triggered.connect(self.new_template)
        icon_newseries= QIcon()
        icon_newseries.addPixmap(QPixmap("graph/newseries.png")), QIcon.Mode.Normal
        self.actionNew_Series_Template.setIcon(icon_newseries)

        self.actionOpen_Series_Template = QAction(MainWindow)
        self.actionOpen_Series_Template.setObjectName("actionOpen_Series_Template")
        self.actionOpen_Series_Template.setText("Open Series Template")
        self.actionOpen_Series_Template.setShortcut("Shift+F5")
        icon_openseries= QIcon()
        icon_openseries.addPixmap(QPixmap("graph/openseries.png")), QIcon.Mode.Normal
        self.actionOpen_Series_Template.setIcon(icon_openseries)
        self.actionOpen_Series_Template.triggered.connect(lambda: self.open_template(""))

        self.menuProject.addAction(self.actionNew_Project)
        self.menuProject.addAction(self.actionOpen_Project)
        self.actionConfig.setText("Config")
        icon_config= QIcon()
        icon_config.addPixmap(QPixmap("graph/settings.png")), QIcon.Mode.Normal
        self.actionConfig.setIcon(icon_config)
                                            
        self.menuSettings.addAction(self.actionNew_Series_Template)
        self.menuSettings.addAction(self.actionOpen_Series_Template)
        self.menuSettings_2.addAction(self.actionConfig)

        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuSettings_2.menuAction())

        self.actionNew_Series_Template.setEnabled(False)
        self.actionOpen_Series_Template.setEnabled(False)
        self.actionConfig.setEnabled(False)

    def start_trigger(self): # Sends a trigger to the photon detector
        self.show_progress_dialog("Mesuremeasurement", "Mesuremeasurement in progress. Please wait.")
        commandTrigger(2000, self.trigger_com)
        sleep(3)
        self.close_progress_dialog()

    def draw_relative_layout(self): # Draws the engine layout in relative mode
        self.clear_window()

        if self.background_thread is not None:
            self.background_worker.stop()
            self.background_thread.quit()
            self.background_thread.wait()

        self.top_bar_frame.setVisible(True)
        self.Move_Button.setVisible(False)
        self.Reset_button.setVisible(True)
        row = 0

        for index, element in enumerate(self.motors_list):
            row = index // 4
            column = index % 4
            if isinstance(element, Rotation_Motor):
                MotorControlWidget = RelativeRotationControlWidget(element.branch, element.function, element)
            else:
                MotorControlWidget = RelativePositionControlWidget(element.branch, element.function, element)

            MotorControlWidget.setFixedSize(240, 120)
            self.grid_layout.addWidget(MotorControlWidget, row, column)

        if row>0:
            self.Polariton_Label.hide()
            self.Polariton_Bar_Label.setVisible(True)
        else:
            self.Polariton_Label.show()
            self.Polariton_Bar_Label.setVisible(False)

        self.create_thread()

    def draw_absolute_layout(self): # Draws the engine layout in absolute mode
        self.clear_window()

        if self.background_thread is not None:
            self.background_worker.stop()
            self.background_thread.quit()
            self.background_thread.wait()
            
        self.top_bar_frame.setVisible(True)
        self.Move_Button.setVisible(True)
        self.Reset_button.setVisible(True)
        row = 0

        for index, element in enumerate(self.motors_list):
            row = index // 4
            column = index % 4
            if isinstance(element, Rotation_Motor):
                MotorControlWidget = AbsoluteRotationControlWidget(element.branch, element.function, element)
            else:
                MotorControlWidget = AbsolutePositionControlWidget(element.branch, element.function, element)

            MotorControlWidget.setFixedSize(230, 230)
            self.grid_layout.addWidget(MotorControlWidget, row, column)

        if row>0:
            self.Polariton_Label.hide()
            self.Polariton_Bar_Label.setVisible(True)
        else:
            self.Polariton_Label.show()
            self.Polariton_Bar_Label.setVisible(False)

        self.create_thread()
    
    def create_thread(self): # Creates a background thread with a Processor object
        self.background_thread = QThread()
        self.background_worker = Processor()
        self.background_worker.moveToThread(self.background_thread)
        self.background_thread.started.connect(self.background_worker.run)
        self.background_thread.finished.connect(self.background_worker.stop)
        self.background_thread.start()

    def new_project(self): # Displays the new project creation window
        self.win = NewProjectWindow()
        self.win.show()
        self.win.closed.connect(lambda: self.open_file(file_name=self.win.path))

    def open_project(self): # Displays the project opening window
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open file", "Projects", "Text Files (*.json);;All Files (*)", options=options
        )
        self.open_file(file_name=file_name)

    def open_file(self, file_name=""): # Opens a file and reads information about engines, creating objects and a list of these objects + runs initSerials
        working_coms=set()
        self.key=""

        for element in self.rotation_motorlist:
            element.clear_self()

        self.motors_list.clear()
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    file_content = file.read()
                    file_content = json.loads(file_content)
                    position_index=0
                    for element in file_content:
                        if element['function']== "Rotation":
                            motor = Rotation_Motor(
                                com=element['com'],
                                pins=element['pins'],
                                branch=element['branch'],
                                function=element['function'],
                                steps_per_revolution=element['StepsPerRevolution'],
                                number=element['StepperNumber'],
                                direction= element['rotationDirection']
                            )
                            self.motors_list.append(motor)
                            self.rotation_motorlist.append(motor)
                            working_coms.add(element['com'])
                            self.key += (element['function'][0]+ str(len(self.rotation_motorlist)))
                        else:
                            motor = Position_Motor(
                                branch=element['branch'],
                                function=element['function'],
                                number=element['StepperNumber'],
                                serial_no=element["serial_no"],
                                index= position_index
                            )
                            self.motors_list.append(motor)
                            self.position_motorlist.append(motor)
                            position_index+=1
                            self.key += (element['function'][0]+ str(len(self.position_motorlist)))
                            
                    self.show_progress_dialog("Motor initialization", "Motors are initialized. Please wait.") 
                    initSerials(working_coms, .1)
                    sleep(2)
                    if  self.control_mode == "Absolute":
                        self.draw_absolute_layout()
                    else:
                        self.draw_relative_layout()
                    sleep(1)
                    InitMotorsFromList(self.rotation_motorlist)
                    Config_Engines(self.position_motorlist)
                    self.close_progress_dialog()
                    self.actionNew_Series_Template.setEnabled(True)
                    self.actionOpen_Series_Template.setEnabled(True)
                    self.actionConfig.setEnabled(True)

            except:
                self.show_error_window("The selected file is invalid")

        else:
            pass
    
    def new_template(self):
        self.win = SeriesCreator(self.key)
        self.win.show()
        self.win.closed.connect(lambda: self.open_template(filename=self.win.path))

    def open_template(self, filename=""): # Open the measurement series template
        file_name = filename
        if file_name == "":
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Open file", "Templates", "Text Files (*.csv);;All Files (*)", options=options
            )

        if file_name:
            if self.background_thread is not None:
                self.background_worker.stop()
                self.background_thread.quit()
                self.background_thread.wait()
                self.background_thread= None

            self.show_progress_dialog("Measurement series", "The measurement series is in progress. Please wait.")
            readCSV(file_name, self.motors_list, self.key, self.trigger_com, self.measurement_time)
            self.draw_layout()
            self.close_progress_dialog()

    def show_progress_dialog(self, Title, Label): # Display the progress window
        self.progress_dialog= ProgresssDialog(Title, Label)
        self.progress_dialog.show()
        app.processEvents()
    
    def close_progress_dialog(self): # Close the progress window
        self.progress_dialog.close()

    def show_error_window(self, msg): # Displays an error message
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("Error")
        msg_box.setInformativeText(msg)
        msg_box.setWindowTitle("Error")
        msg_box.resize(150, 50)
        msg_box.exec()

    def reset_position(self): # Sets motors to zero position    
        self.show_progress_dialog("Motors moving", "Motors are in motion. Please wait.")
        for i, element in enumerate(self.motors_list):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(element,Rotation_Motor):
                if element.angle != 0:
                    moveToAngle(element, 0)
                    element.angle = 0
                    widget.actual_position_display.setText(str(0) + " ps")
            else:
                if element.position != 0:
                    Homing(element.index)
                    element.position = 0
                    widget.actual_position_display.setText(str(0) + " °")
            if self.control_mode=="Absolute":
                widget.position_slider.setValue(0)
        sleep(5)
        self.close_progress_dialog()

    def change_position(self): # Moves motors to target positions
        self.show_progress_dialog("Motors moving", "Motors are in motion. Please wait.")
        for i, element in enumerate(self.motors_list):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(element,Rotation_Motor):
                if element.angle != int(widget.target_position_display.text()):
                    moveToAngle(element, int(widget.target_position_display.text()))
                    element.angle = int(widget.target_position_display.text())
                    widget.actual_position_display.setText(str(element.angle) + " °")
                    sleep(1)
            else:
                if element.position != int(widget.target_position_display.text()):
                    Move_to_Position(element.index, int(widget.target_position_display.text()))
                    element.position = int(widget.target_position_display.text())
                    widget.actual_position_display.setText(str(element.position) +" ps")
                    sleep(1)
        self.close_progress_dialog()

    def clear_window(self): # Removes all widgets from the main interface 
        self.top_bar_frame.setVisible(False)
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, AbsoluteRotationControlWidget):
                widget.deleteLater()
            if isinstance(widget, AbsolutePositionControlWidget):
                widget.deleteLater()
            if isinstance(widget, RelativeRotationControlWidget):
                widget.deleteLater()
            if isinstance(widget, RelativePositionControlWidget):
                widget.deleteLater()


    def open_config_dialog(self): # Opens a window with config settings
        settings_dialog = SettingsDialog(mode= self.control_mode, com= self.trigger_com, time=self.measurement_time)
        settings_dialog.controlModeChanged.connect(self.on_control_mode_changed)
        settings_dialog.exec()

    def draw_layout(self): # Draws main interface
        if self.control_mode == "Relative":
            self.draw_relative_layout()

        elif self.control_mode == "Absolute":
            self.draw_absolute_layout()

    def on_control_mode_changed(self, selected): # Function that applies changes from the config
        self.control_mode= selected[0]
        if selected[0] == "Relative":
            self.draw_relative_layout()
        elif selected[0] == "Absolute":
            self.draw_absolute_layout()

        self.trigger_com= selected[1]
        self.measurement_time = selected[2]

if __name__ == "__main__": #main
    import sys
    app = QtWidgets.QApplication(sys.argv)
    from Position_Controler import Config_Engines, Homing, Move_to_Position, Close_Connection
    from relative_control_widgets import RelativeRotationControlWidget, RelativePositionControlWidget
    from SeriesReader import readCSV
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
