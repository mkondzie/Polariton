#include <Stepper.h>

const int numSteppers = 2;
const int TRIGGERPIN = 13;

// Create an array of pointers to Stepper objects. 
// This allows for using more stepper motors than two (which works for Arduino Uno)
Stepper *STEPPERS[numSteppers];

void setup() {
  Serial.begin(9600);
  digitalWrite(TRIGGERPIN, LOW);
  pinMode(TRIGGERPIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    receiveString(); // Receive a string from Python program over serial
    processCommands();      // Process the received commands
  }
}

String mainString = "";

void receiveString() {
  if (Serial.available()) {
    String receivedString = Serial.readString();
    mainString += receivedString; // Append received strings to the mainString
  }
}

void processCommands() {
  String inputString = mainString;

  String substrings[10];
  int substringCount = splitString(inputString, '#', substrings, 10);

  // Process each extracted substring
  for (int i = 0; i < substringCount; i++) {
    char firstCharacter = substrings[i].charAt(0);     // Get the first character of the string to determine which command was sent
    String restOfString = substrings[i].substring(1);  // Get the rest of the string after the first character. This is the command's content
    restOfString = restOfString.substring(1);

    if (firstCharacter == 's') {

      String motor_settings[2];
      int substringCount_pins = splitString(restOfString, ',', motor_settings, 2);
      int steps = motor_settings[1].toInt();
      int index = motor_settings[0].toInt()
      rotateStepper(steps, index); // Rotate the stepper motor

    } else if (firstCharacter == 'c') {

      String pins[7];
      int substringCount_pins = splitString(restOfString, ',', pins, 7);
      int stepperPins[7];
      for (int i = 0; i < 7; i++) {
        stepperPins[i] = pins[i].toInt();
      }
      int index = stepperPins[0];
      STEPPERS[index] = NULL;
      STEPPERS[index] = new Stepper(stepperPins[1], stepperPins[2], stepperPins[3], stepperPins[4], stepperPins[5]);
      STEPPERS[index]->setSpeed(stepperPins[6]); // Create and configure a stepper motor

    } else if (firstCharacter == 't') {
      int restOfString1 = restOfString.toInt();
      digitalWrite(TRIGGERPIN, HIGH);
      delay(restOfString1); // Set one pin to HIGH to trigger a measurement
      digitalWrite(TRIGGERPIN, LOW);
    }
    
    mainString = ""; // Reset the main string for the next set of commands
    Serial.print(substrings[i]);
  }
}

// Split a string into substrings using a delimiter character
int splitString(String inputString, char delimiter, String *substrings, int maxSubstrings) {
  int count = 0;
  int startIndex = 0;
  int endIndex = inputString.indexOf(delimiter);

  while (endIndex >= 0 && count < maxSubstrings - 1) {
    substrings[count++] = inputString.substring(startIndex, endIndex);
    startIndex = endIndex + 1;
    endIndex = inputString.indexOf(delimiter, startIndex);
  }

  // Handle the last substring after the last delimiter
  if (startIndex < inputString.length() && count < maxSubstrings) {
    substrings[count++] = inputString.substring(startIndex);
  }

  return count;
}

// Rotate a stepper motor by a specified number of steps
// Index differentiates between motors on the same board
void rotateStepper(int steps, int index) {
  STEPPERS[index]->step(steps);
}
