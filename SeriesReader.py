import csv
from Motors import Rotation_Motor, Position_Motor
from CommandCenter import commandMove, moveToAngle, Process_Commands, commandTrigger, commandMove
from Position_Controler import Move_to_Position
from time import sleep
from timer import Timer
from PySide6.QtWidgets import QMessageBox

# Function to display an error window with the given message
def show_error_window(msg):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("Error")
        msg_box.setInformativeText(msg)
        msg_box.setWindowTitle("Error")
        msg_box.resize(150, 50)
        msg_box.exec()

# Function to wait for the processor to send all commands
def wait_for_processor():
    working_status= True
    while working_status:
        if (Process_Commands()):
            working_status=False
            return 1
        print("Waiting for laser data")
    return 0

# Function to read data from a CSV file and execute corresponding commands
def readCSV(file, motors, key, com, time):
    print(time)
    with open(file, mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for index, row in enumerate(reader):
            sleep(1)
            if index==0:
                row0 = row
                Key = "".join(row).strip()
                if key != Key:
                    show_error_window("Wrong project")
                    return -1
                Motors = {}

                for motor_name in row:
                    if motor_name[0] == "R":
                        motor = [m for m in motors if (isinstance(m,Rotation_Motor) and int(motor_name[1:]) == m.number)]
                    elif motor_name[0] == "P":
                        motor = [m for m in motors if (isinstance(m,Position_Motor) and int(motor_name[1:]) == m.index+1)]

                    Motors[motor_name]=motor

            else:
                repeat = row[-1]
                for _ in range(int(repeat)):
                    for column_index,element in enumerate(row[:-1]):
                        execute(Motors[row0[column_index]][0], element)
                        print(f"Motor Name: {row0[column_index]}, Move to: {element}, Motor object: {Motors[row0[column_index]][0]}, {repeat} times")
                                  
                    wait_for_processor()
                    sleep(5)
                    commandTrigger(2000, com)
                    wait_for_processor()
                    sleep(int(time))

# Function to move a motor
def execute(motor, command):
    command = int(command)
    if isinstance(motor, Rotation_Motor):
        commandMove(motor, command)
    else:
        if motor.position + command > 320:
            Move_to_Position(motor.index, 320)
            motor.position = 320

        elif motor.position + command < 0:
            Move_to_Position(motor.index, 0)
            motor.position += 0

        else:
            Move_to_Position(motor.index, motor.position + command)
            motor.position += command


