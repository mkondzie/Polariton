import os
import time
import sys
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll.")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll.")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll.")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.BrushlessMotorCLI import *
from System import Decimal

cubes_list=[]
motors_list=[]

def Config_Engines(motor_list): # Configures KCubeBrushlessMotor devices
    try:
        DeviceManagerCLI.BuildDeviceList()
        for element in motor_list:
            serial_no = element.serial_no  
            motors_list.append(element)
            kcube = KCubeBrushlessMotor.CreateKCubeBrushlessMotor(serial_no)
            cubes_list.append(kcube)
            kcube.Connect(serial_no)
            time.sleep(0.25)
            kcube.StartPolling(250)
            time.sleep(0.25)
            kcube.EnableDevice()
            time.sleep(0.25)
            device_info = kcube.GetDeviceInfo()
            print(device_info.Description)
            if not kcube.IsSettingsInitialized():
                kcube.WaitForSettingsInitialized(10000)  
                assert kcube.IsSettingsInitialized() is True
            Homing(element.index)
    except Exception as e:
        print(e)

def Homing(index): # Initiates homing for a specified motor.
    try:
        m_config = cubes_list[index].LoadMotorConfiguration(motors_list[index].serial_no,
                                                DeviceConfiguration.DeviceSettingsUseOptionType.UseDeviceSettings)

        time.sleep(1)

        print("Homing Device...")
        cubes_list[index].Home(60000)
        print("Device Homed")
    except Exception as e:
        print(e)

def Move_to_Position(index, delay): # Moves the motor to a specified position based on the delay.
    try:
        m_config = cubes_list[index].LoadMotorConfiguration(motors_list[index].serial_no,
                                                DeviceConfiguration.DeviceSettingsUseOptionType.UseDeviceSettings)
        print("Moving Device...")
        # time using speed of light
        # t = s / v
        v = 0.299792458  # mm/ps
        s = delay * v
        pos = Decimal(s) 
        cubes_list[index].MoveTo(pos, 60000)  

        print("Device Moved, Delay in ps: ")
        print(delay)
    except Exception as e:
        print(e)
    
def Close_Connection(): # Closes the connection with all connected KCubeBrushlessMotor devices.
    for element in cubes_list:
        element.StopPolling()
        element.Disconnect(True)
