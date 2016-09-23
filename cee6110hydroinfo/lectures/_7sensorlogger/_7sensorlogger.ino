/*
Timing Example 2
Test sketch to demonstrate how the timing functions work
Created By:  Jeff Horsburgh
Creation Date: 8/13/2016
*/
// Include the DHT sensor library
#include "DHT.h"
#include <SD.h>


// Define the digital pin you are connecting the DHT sensor to
#define DHTPin 2 

// The DHT library supports multiple DHT sensors, so need to 
// define the type of sensor we are using
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

// Initialize DHT sensor using the pin and sensor type
DHT dht(DHTPin, DHTTYPE);

// Declare some needed variables
int scanInterval = 5;   // Time between scans within the main loop in seconds
int recordInterval = 10; // Time between recorded values in seconds
unsigned long currMicros = 0;       // Timing variable
unsigned long prevMicros = 0;       // Timing variable
unsigned long prevRecordMicros = 0; // Timing variable
int scanCounter = 0;   // A variable to hold a count of scans
int recordCounter = 0; // A variable to hold a count of output records
float randomNum;       // Variable to hold a random number
float HumSum;       // Variable to enable calculation of the average value for randNum
float avgHum;    // Variable to hold the average value of randNum
float TempSum;
float avgTemp;


void setup(){
  // Create a serial port and print a header line
  Serial.begin(9600);
  Serial.println("Temperature and Relative Humidity Sensor Output");
  Serial.println("Measurements using a DHT22 Sensor");
  Serial.println("ScanNumber, Temperature, Humidity"); // Write column headers to output table
  pinMode(10, OUTPUT); // Set the pinMode on digital pin 10 to OUTPUT
  // Begin communication with the DHT sensor
  if (!SD.begin(10)){
    Serial.println("SD card initialization failed!");
    return;
  }
  File myFile = SD.open("7exp.txt", FILE_WRITE);
  myFile.println("RecordNumber, Humidity, Temperature");
  myFile.close();
  dht.begin();
}

void loop(){
  // Get the current time 
  // (number of microseconds since the program started)
  File myFile = SD.open("7exp.txt", FILE_WRITE);
  currMicros = micros();

  // Check timing to see if the scan interval has been reached
  if ((currMicros - prevMicros) >= (scanInterval * 1000000))
  {
    // If YES, do a scan
    // -----------------  
    // Increment the scan counter variable
    scanCounter ++;  // The "++" operator adds 1 to a variable

    // Perform measurements and calculations here
    // ------------------------------------------
    // We don't have any sensors yet, so just generate a random number
    //    randomNum = random(1, 10);  // Create a random number between 1 and 10
    //HumSum += randomNum;     // Add the current random number to a sum 
    // Get the most recent measurements from the sensor
    float hum = dht.readHumidity();  // Get the humidity value in percent
    HumSum += hum;
    float degC = dht.readTemperature(); // Get the temperature value in Celisius
    TempSum += degC;
    // The sensor will also return the temperature as Fahrenheit (isFahrenheit = true)
    float degF = dht.readTemperature(true);

    // Create a string with output for this scan to print to the serial port
    // Use the "+" operator to concatenate strings together
    // The "String()" function converts numbers to strings
    String stringToPrint = String(scanCounter) + ", " + hum + ", " + degC;
    Serial.println(stringToPrint);

    // Manage the timing variables to reflect that I just finished a scan
    prevMicros = currMicros;

    // Check to see if it's time to record data
    if ((currMicros - prevRecordMicros) >= (recordInterval * 1000000))
    {
      // Record a data record - for now print to the serial port 
      // A later example will show how to write to a file
      // ----------------------------------------------------------------
      // Calculate the average value of the random number
      avgHum = HumSum / scanCounter;
      avgTemp = TempSum / scanCounter;
      // Increment the record counter
      recordCounter ++;
      
      // Create a string to record the output data to the serial port
      String recordToPrint = "RecordNumber = " + String(recordCounter) + \
                             ", ElapsedTime (us) = " + String(currMicros) + \
                             ", Humidity = " + String(avgHum) + "TempinC = " + String(avgTemp);
      Serial.println(recordToPrint);
      myFile.println(recordToPrint);
      
      // Manage to timing variables to reflect that I just recorded data
      // and reset the scanCounter and randomSum variables for the next scan
      prevRecordMicros = currMicros;
      scanCounter = 0;
      HumSum = 0;
      TempSum=0;
    }
  } 
  myFile.close();
}
