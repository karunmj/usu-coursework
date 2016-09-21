/*
Test sketch to demonstrate how the timing functions work
Created By:  Jeff Horsburgh
Creation Date: 8/12/2016
*/

// Create a long integer variable to store the number of milliseconds
unsigned long time;

void setup(){
  // Create a serial port and print a header line
  Serial.begin(9600);
  Serial.println("Timing Test Sketch Output");
}

void loop(){
  Serial.print("Time: ");
  
  // Set the "time" variable to the number of milliseconds since the 
  // program started by calling the millis() function
  time = millis();
  
  // Prints the time since program started to the serial monitor
  Serial.println(time);
  
  // wait a second so as not to send massive amounts of data
  delay(1000);
}
