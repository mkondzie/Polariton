# Polariton

Polariton is a customizable experimental setup control app that allows for changing the angles and positions of motors connected to microcontrollers.

## Description

The Polariton app provides a graphical user interface and serial communication with stepper motors connected to Arduino and Thorlabs optical delay lines. When used with continuous neutral density filters mounted on stepper motors, the rotation angle controls the intensity of the laser beam. The optical delay line can be controlled by specifying the desired delay time in picoseconds.

### Requirements

Before installing the Polariton app, you'll need the following:

* [Arduino IDE](https://www.arduino.cc/en/software)
* [Kinesis Software](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10285)
* Python.NET - Install it by opening the command prompt and running
```
pip install pythonnet 
```

If you encounter any issues, you may need to uninstall the 'clr' package

```
pip uninstall clr
```

## Getting Started

First, please make sure that your stepper motors are powered and connected to the correct digital pins according to the manufacturer's instructions (usually in ascending order with the controller board). Then, open .IDE file and upload the project on all connected Arduino boards.
To get started, create a new file that represents your experimental setup.



## Authors

* Olgierd Jeziorski
* Maria Kondzielska
* Jakub Rogala

## Project coordinator

* Krzysztof Tyszka

## Report
[Experimental setup for delay, division and modulation of laser pulses:
emission from polariton condensate pumped with a pulsed laser](https://mycloud.fuw.edu.pl/index.php/s/MBf3fFp8NWrFQxE#pdfviewer)

## Acknowledgments

* [Thorlabs Motion Control Examples](https://github.com/Thorlabs/Motion_Control_Examples)
* [The 28BYJ-48 Stepper Motor](https://lastminuteengineers.com/28byj48-stepper-motor-arduino-tutorial/)
