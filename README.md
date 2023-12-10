# Polariton

Polariton is a customizable experimental setup control app that allows for changing the angles and positions of motors connected to microcontrollers.

## Description

The Polariton app provides a graphical user interface and serial communication with stepper motors connected to Arduino and Thorlabs optical delay lines. When used with continuous neutral density filters mounted on stepper motors, the rotation angle controls the intensity of the laser beam. The optical delay line can be controlled by specifying the desired delay time in picoseconds.

### Requirements

Before installing the Polariton app, you'll need the following:

* [Arduino IDE](https://www.arduino.cc/en/software)
* [Kinesis Software](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10285)
  

If you encounter any issues, please make sure you have all the necessary libraries installed.

You may need to uninstall the 'clr' package:

```
pip uninstall clr
```

and install Python.NET:
```
pip install pythonnet 
```

## Getting Started

First, please make sure that your stepper motors are powered and connected to the correct digital pins according to the manufacturer's instructions (usually in ascending order with the controller board). Then, open the provided .ino file with Arduino IDE and [upload](https://support.arduino.cc/hc/en-us/articles/4733418441116-Upload-a-sketch-in-Arduino-IDE) the project on all connected Arduino boards.


When you first run the Polariton app, you'll see the welcome screen.
<img width="764" alt="welcome" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/2b233e59-01de-452d-8807-678e6f5bb3cd">

Here you can select "File" and create a "New Project".
 <img width="764" alt="select" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/799ce15f-b7fb-4e7f-85c6-26b78b80516b">




To get started, create a new file that represents your experimental setup. All available ports will be detected automatically. All you need to do is select the port from the drop-down list.
Rotation motors need to have specified pins. Rotation direction can be changed.

<img width="380" alt="create" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/2353d0cf-8758-4489-9903-c7481cef8d2d">




The default number of steps per revolution is 64 and can be changed according to your stepper motor specification.



Positional motors (delay lines) require a serial number. In case of Thorlabs KBD101 Driver, the serial number is located on the back of the cube:


<img width="350" alt="serial_no" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/d1cdf009-4fe1-49bb-b1bb-a11c4b122176">

[Source](https://www.thorlabs.com/_sd.cfm?fileName=TTN126351-D02.pdf&partNumber=ODL100)

When the projects is complete, you need to save it ("Projects" folder is generated automatically). Default name of a project is generated as follows: YYYY-MM-DD-_HH-MM.
Later on, when you have a set of projects, you can also edit a saved project or save it once more to enter the initialization phase.
Please note that pins and coms are **NOT** kept when you open saved project files, so you need to select them manually every time you edit a project.

<img width="475" alt="edit" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/88ca879b-e7e7-4623-ae18-1de9f6c8ed04">

<img width="760" alt="init" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/a3bf7fb4-eb97-4353-876e-517afb69c8d2">

In relative mode, we're able to select the increment (multiples of 5 degrees or picoseconds) of motion.  To move a motor, click the left or right arrow, specifying direction.



<img width="760" alt="relative" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/b1096a28-4d22-4294-b90a-4cb1e01944b9">

When we click "Reset position", all motors will move back to zero.
<img width="761" alt="reset" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/0efa3ba7-2c26-43df-b26f-57f4e0e08f27">


To enter the absolute mode, first select Settings>Config.
<img width="762" alt="config" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/5c8344f2-df41-4264-80d3-c82e2969fe1e">

Then in the "Control Mode"  drop-down list you select "Absolute". Trigger com can be selected to control [SPC](https://www.becker-hickl.com/products/tcspc-package/) measurements. Measurement time can be provided, keeping in mind that Arduino takes time to process commands. The default value is 2 seconds.

<img width="761" alt="settings_abs" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/5fc449a2-af0c-44e8-9935-3b6a90f8551b">

In absolute mode, target angles and delays can be selected. To execute these commands, you need to press "Move motors".

<img width="759" alt="move" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/f42f81f3-1296-4e92-98b6-fc4cc4710d9c">

To measure, e.g. single photons and time delay between laser pulses, in [SPC](https://www.becker-hickl.com/products/tcspc-package/) "System Parameters" you need to select ascending trigger and correct saving to .sdt file options. 


![trigger_save_file](https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/14031aa3-7dd8-4ea9-ac4b-abbedd8fec38)


At the top, click "Start!", and then back in the Polariton app click the "Measure" button:


![SPC_start](https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/53362043-20c8-4767-b9b1-47230efde8aa)



<img width="762" alt="measure" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/ed0c9fd9-fbca-409a-b9b3-bccef69aa064">

Another available option is "Run", where you can create your own measurement series template.

<img width="762" alt="run" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/1f233a0b-312d-48fb-92cd-4d08f913277f">


You can add action, which consists of commands for each motor. Additionally, you can specify the number of repetitions for each action. "R" stands for rotation motors, while "P" stands for positional motors.
<img width="760" alt="new_series" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/087cf634-3be5-4bc5-87a7-017405cb8d58">

When you are ready for the measurement series, i.e. in [SPC](https://www.becker-hickl.com/products/tcspc-package/) "System Parameters" you selected ascending trigger and correct file saving options. 


![trigger_save_file](https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/14031aa3-7dd8-4ea9-ac4b-abbedd8fec38)


Also, you clicked "Start!":

![SPC_start](https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/53362043-20c8-4767-b9b1-47230efde8aa)

Then, you can press "Save and Run" to start taking data. 


<img width="764" alt="save_run" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/fd95a8e0-b645-4ef2-b6a7-8f4b5ca5717f">

Another possibility is "Open Series Template", which allows you to select saved series (default folder is auto-generated "Templates"). 

<img width="762" alt="run" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/5e97a483-1a20-42fd-8b25-4729af75418e">

The file naming convention remains YYYY-MM-DD-_HH-MM.

<img width="761" alt="open_template" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/95fd77d9-eb95-4316-930d-a319820f75db">

Immediately after opening, the measurement series starts. Therefore, make sure to select ascending trigger and correct file saving options in [SPC](https://www.becker-hickl.com/products/tcspc-package/) and click "Start!" **before opening a saved template**.
<img width="761" alt="measure_from_template" src="https://github.com/jakrog01/Warsztaty-Wakacyjne/assets/141751789/f0ebeaa2-697d-45fd-a743-3aab21cbabc0">



When you close the Polariton app, by default all motors return back to zero positions.
## Authors

* Olgierd Jeziorski
* Maria Kondzielska
* Jakub Rogala

## Project coordinator

* Krzysztof Tyszka



## Acknowledgments

* [Thorlabs Motion Control Examples](https://github.com/Thorlabs/Motion_Control_Examples)
* [The 28BYJ-48 Stepper Motor](https://lastminuteengineers.com/28byj48-stepper-motor-arduino-tutorial/)

