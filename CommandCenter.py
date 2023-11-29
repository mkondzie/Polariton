import serial
from time import sleep, perf_counter
from Motors import Rotation_Motor
import Motors
from timer import Timer

Working_COMs = {} # Dictionary to store active communication ports
MaxCommandsInsideArduino = 1 # Maximum number of commands allowed inside Arduino

class Command: # Class for representing commands and managing their status
    all = []
    Catalogue = {"pending": 0, "sent": 0, "done": 0}
    COMCatalogue = {}

    def __init__(self, content, com, delay=0):
        self.content = content
        self.com = com
        self.delay = delay
        self.status = "Pending"
        self.signature = str(self.com) + str(self.content)[:-1]  # Służy do rozpoznawania komend, które zostały wykonane
        self.id = len(Command.all)

        if self.com not in Command.COMCatalogue:
            Command.COMCatalogue[self.com] = {"pending": 0, "sent": 0, "done": 0}

        Command.Catalogue["pending"] += 1
        Command.COMCatalogue[self.com]["pending"] += 1

        Command.all.append(self)

    def send(self):
        Working_COMs[self.com].write(self.content.encode() + b'\n')  # Encode and send data to Arduino with newline
        print("Sent")
        self.status = "Sent"
        Command.Catalogue["sent"] += 1
        Command.COMCatalogue[self.com]["sent"] += 1

    def markAsDone(self): # Mark the command as done and update catalog counts
        print("Done")
        self.status = "Done"
        Command.Catalogue["done"] += 1
        Command.COMCatalogue[self.com]["done"] += 1

        self.delete()

    def delete(self):
        Command.all.remove(self)
        del self

def listen():  # Function to listen for data from Arduino on active communication ports
    result = []
    for com in Working_COMs:
        data = Working_COMs[com].readline().decode().strip()
        data = str(com) + str(data)
        result.append(data)
    return result

def Process_Commands(): # Process commands and manage their execution
    receivedData = listen()
    print(f"Received: {receivedData}")
    for command in Command.all:
        if command.status == "Waiting for completion":
            if perf_counter()-command.startTime >= command.delay:
                command.markAsDone()

        if command.signature in receivedData and command.status == "Sent":
            print(f"Signature ({command.signature}) found")
            command.status = "Waiting for completion"
            command.startTime = perf_counter()

        if command.status == "Pending" and Command.COMCatalogue[command.com]["sent"] - \
                Command.COMCatalogue[command.com]["done"] < MaxCommandsInsideArduino:
            command.send()
            print(f"Command ({command.content}) sent")
            sleep(command.delay)

    for COM in Command.COMCatalogue:
        if Command.COMCatalogue[COM]["pending"] == Command.COMCatalogue[COM]["done"]:
            print(f"Done on {COM}")
            pass
    if Command.Catalogue["pending"] == Command.Catalogue["done"]:
        print(f"Done on all COMs")
        return True  # Return True when all commands have been sent and received
    else:
        print("Working")
        print("!!!!!!!!!!!", [(c.content, c.com) for c in Command.all])
        return False

def initSerials(UsedComs, Timeout=1): # Initialize serial communication for specified COM ports
    for com in UsedComs:
        if com in Working_COMs:
            Working_COMs[com].close()
        Working_COMs[com] = serial.Serial(com, 9600,timeout=Timeout) 
    
def commandConfig(motor):  # Configure a motor and send the configuration data to Arduino

    pins = motor.pins
    data = f"c,{motor.index},{motor.steps_per_revolution},{pins[0]},{pins[1]},{pins[2]},{pins[3]},{motor.velocity}#"

    Command(data, motor.com, delay=0)

def commandTrigger(delay,  com): # Trigger a command with a specified delay on a communication port
    Command(f"t,{delay}#", com)        #delay in milisecs


def commandMove(motor, angle):  # Move a motor by a specified angle
    steps = angle * (2038 / 360)
    steps = int(steps)
    if (motor.direction != 'Right'):
        steps = -steps
    print(angle)
    data = f"s,{motor.index},{steps}#"

    # send_to_arduino(data, motor.com)
    Command(data, motor.com, delay=(abs(
        (9.8 / 2038) * steps)))
    motor.rotate(angle)

def moveToAngle(motor, angle): # Move a motor to a specified angle

    angle %= 360  

    Angle = angle - motor.angle

    commandMove(motor, Angle)

def InitMotorsFromList(list):  # Initialize motors based on a provided list of information
    for element in list:
        if isinstance(element, Rotation_Motor):
            commandConfig(element)

def setRTSforSerial(com): # Set RTS for a serial communication port
    Working_COMs[com].setRTS(True)
    sleep(1)
    Working_COMs[com].setRTS(False)
