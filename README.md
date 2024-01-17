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
<img width="764" alt="1" src="https://github.com/jakrog01/Polariton/assets/141751789/f73caf5e-e547-4843-9f5d-0a01d00e034d">


Here you can select "File" and create a "New Project".
<img width="764" alt="2" src="https://github.com/jakrog01/Polariton/assets/141751789/6a18d6ac-af82-4c47-b9ba-93e0df242031">



To get started, create a new file that represents your experimental setup. All available ports will be detected automatically. All you need to do is select the port from the drop-down list.
Rotation motors need to have specified pins. Rotation direction can be changed.



<img width="456" alt="3" src="https://github.com/jakrog01/Polariton/assets/141751789/2d2cf2e5-9612-4388-995b-7cf7e6f8c2f8">



The default number of steps per revolution is 64 and can be changed according to your stepper motor specification.



Positional motors (delay lines) require a serial number. In case of Thorlabs KBD101 Driver, the serial number is located on the back of the cube:

<img width="553" alt="4" src="https://github.com/jakrog01/Polariton/assets/141751789/302ea0d7-41d6-4666-a82b-733fc6adb7f7">

[Source](https://www.thorlabs.com/_sd.cfm?fileName=TTN126351-D02.pdf&partNumber=ODL100)

When the projects is complete, you need to save it ("Projects" folder is generated automatically). Default name of a project is generated as follows: YYYY-MM-DD-_HH-MM.
Later on, when you have a set of projects, you can also edit a saved project or save it once more to enter the initialization phase.
Please note that pins and coms are **NOT** kept when you open saved project files, so you need to select them manually every time you edit a project.
<img width="475" alt="5" src="https://github.com/jakrog01/Polariton/assets/141751789/1934ca6e-a62d-4e15-ba95-247e92d2963c">

<img width="760" alt="6" src="https://github.com/jakrog01/Polariton/assets/141751789/b9d0a263-8584-480f-97c5-bd301faea1b1">


In relative mode, we're able to select the increment (multiples of 5 degrees or picoseconds) of motion.  To move a motor, click the left or right arrow, specifying direction.


<img width="762" alt="7" src="https://github.com/jakrog01/Polariton/assets/141751789/99181ab9-faa5-427a-9531-02c8c836db2b">

When we click "Reset position", all motors will move back to zero.

<img width="761" alt="8" src="https://github.com/jakrog01/Polariton/assets/141751789/22ef0504-40c8-4404-96eb-ae0a7abf5593">

To enter the absolute mode, first select Settings>Config.
<img width="762" alt="9" src="https://github.com/jakrog01/Polariton/assets/141751789/1cd08c18-ba2f-4db4-9533-bf14965e6ca6">

Then in the "Control Mode"  drop-down list you select "Absolute". Trigger com can be selected to control [SPC](https://www.becker-hickl.com/products/tcspc-package/) measurements. Measurement time can be provided, keeping in mind that Arduino takes time to process commands. The default value is 2 seconds.

<img width="761" alt="10" src="https://github.com/jakrog01/Polariton/assets/141751789/419c4886-9f84-413f-99c8-45613867ab6a">

In absolute mode, target angles and delays can be selected. To execute these commands, you need to press "Move motors".

<img width="759" alt="11" src="https://github.com/jakrog01/Polariton/assets/141751789/1ae3b91d-e20b-4022-ad7d-5cecf2c59d2c">

To measure, e.g. single photons and time delay between laser pulses, in [SPC](https://www.becker-hickl.com/products/tcspc-package/) "System Parameters" you need to select ascending trigger and correct saving to .sdt file options. 


![12](https://github.com/jakrog01/Polariton/assets/141751789/6c57f211-6f79-4769-b16a-936ea1212bc3)


At the top, click "Start!", and then back in the Polariton app click the "Measure" button:

![13](https://github.com/jakrog01/Polariton/assets/141751789/91520b67-e7dd-49c9-95f3-9d2e2db141f7)


<img width="762" alt="14" src="https://github.com/jakrog01/Polariton/assets/141751789/1a6bd203-b9ee-407c-979c-5ea661f9e071">

Another available option is "Run", where you can create your own measurement series template.

<img width="762" alt="15" src="https://github.com/jakrog01/Polariton/assets/141751789/71667f00-88f7-4dde-924a-ae7c682ba95e">


You can add action, which consists of commands for each motor. Additionally, you can specify the number of repetitions for each action. "R" stands for rotation motors, while "P" stands for positional motors.
<img width="760" alt="16" src="https://github.com/jakrog01/Polariton/assets/141751789/3ab9fe13-662e-4fcf-8034-088f1a727cde">

When you are ready for the measurement series, i.e. in [SPC](https://www.becker-hickl.com/products/tcspc-package/) "System Parameters", make sure you selected ascending trigger and correct file saving options. 


![12](https://github.com/jakrog01/Polariton/assets/141751789/ee4a8e31-0fd7-4025-9bb3-77a2f9870734)


Also, make sure you clicked "Start!":
![13](https://github.com/jakrog01/Polariton/assets/141751789/8d5d384d-98ea-4cea-8fd7-92c1249f9f5b)


Then, you can press "Save and Run" to start taking data. 


<img width="764" alt="17" src="https://github.com/jakrog01/Polariton/assets/141751789/1bc53d83-8e95-4ea8-bec4-399bd53e337b">

Another possibility is "Open Series Template", which allows you to select saved series (default folder is auto-generated "Templates"). 

<img width="762" alt="18" src="https://github.com/jakrog01/Polariton/assets/141751789/80d3263b-c2d2-4ab7-bd5b-f2cd1da385fd">

The file naming convention remains YYYY-MM-DD-_HH-MM.

<img width="761" alt="19" src="https://github.com/jakrog01/Polariton/assets/141751789/be91d3f0-9cea-4b18-b257-dcb1005a8c43">

Immediately after opening, the measurement series starts. Therefore, make sure to select ascending trigger and correct file saving options in [SPC](https://www.becker-hickl.com/products/tcspc-package/) and click "Start!" **before opening a saved template**.

<img width="761" alt="20" src="https://github.com/jakrog01/Polariton/assets/141751789/cd3305f5-d89b-487d-a523-2ecefb871805">



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

