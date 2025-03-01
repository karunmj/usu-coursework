/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the Uno and
  Leonardo, it is attached to digital pin 13. If you're unsure what
  pin the on-board LED is connected to on your Arduino model, check
  the documentation at http://www.arduino.cc

  This example code is in the public domain.

  Modified 12 August 2016
  by Jeff Horsburgh
 */

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  pinMode(13, OUTPUT);

  // initialize a serial port
  Serial.begin(9600);
  // print a header line to the serial port
  Serial.println("This is the output of the Blink Arduino sketch.");
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)
  Serial.println("The LED is on."); // print a message to the serial port
  delay(1000);              // wait for a second
  
  digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
  Serial.println("The LED is off.");
  delay(1000);              // wait for a second
}
