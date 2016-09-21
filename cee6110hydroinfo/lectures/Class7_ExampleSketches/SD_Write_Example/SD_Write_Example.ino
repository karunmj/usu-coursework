/*
MicroSD Card Writing Example
Example of Writing Data to a MicroSD Card Via the Breakout
Created By:  Jeff Horsburgh
Creation Date: 8/14/2016

SDCard Breakout Wiring:
-----------------------
Breakout CS  --> Arduino Digital Port 10
Breakout DI  --> Arduino Digital Port 11
Breakout DO  --> Arduino Digital Port 12
Breakout CLK --> Arduino Digital Port 13
Breakout GND --> Arduino GND
Breakout 5V  --> Arduino 5V
*/

// Include the SD library
#include <SD.h>

// Initialize some variables for use in my main loop
int recordNum = 1;
float someValue = 1.0;

void setup() {
  // Set up a Serial port for output
  Serial.begin(9600);
  Serial.println("Initializing the SD card...");
  
  // Initialize the SD Card
  pinMode(10, OUTPUT); // Set the pinMode on digital pin 10 to OUTPUT
  // Attemt to open a connection to the SD card, if it fails, 
  // send a message to the serial port and exit the program
  if (!SD.begin(10)){
    Serial.println("SD card initialization failed!");
    return;
  }
  
  // Initialization of the SD card was successful
  Serial.println("SD card initialization done.");

  // Create a new file on the SD card to which you want to write
  // Only one file can be open at a time
  // If you want to use a different file, close this one first
  File myFile = SD.open("test.txt", FILE_WRITE);

  // Print a line of text to the open file
  // Also send the text to the serial port so we can see what's going on
  myFile.println("This is how you write a line to a file.");
  Serial.println("This is how you write a line to a file.");
  
  // Print a header line to the file with column names
  myFile.println("RecordNumber, SomeRandomNumber");
  Serial.println("RecordNumber, SomeRandomNumber");
  
  // Close the file 
  myFile.close();
}

void loop() {
  // You can also write data to the file within the main loop
  // For example if you want to write out the most recent observations
  // for a recording interval. 
  
  // Open the file again
  File myFile = SD.open("test.txt", FILE_WRITE);

  // Create a line of comma delimited text to write to the file
  // You would replace this with your sensor measurements
  String dataRecord = String(recordNum) + ", " + String(someValue);

  // Write the dataRecord as a new line to the file
  // Send dataRecord to the serial port as well so we can see it
  myFile.println(dataRecord);
  Serial.println(dataRecord);

  // Close the file
  myFile.close();

  // Increment the recordNumber and set the value of someValue to a
  // random number between 0 and 100
  recordNum ++;
  someValue = random(0, 100);

  // Delay so we don't send too much data
  delay(2000);

}
