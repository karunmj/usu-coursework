/*
Data logger programming and data collection
CEE6110 Assignment#2
Karun Joseph, A02240287
*/

// Include DHT sensor, SD library
#include <DHT.h>
#include <SD.h>

// Define DHT sensor digital pin to 2
#define DHTPin 2 

// Define type of DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

// Initialize DHT sensor using pin and sensor type
DHT dht(DHTPin, DHTTYPE);

// Declare timing variables
int scanInterval = 5;   // Time between scans within the main loop in seconds
int recordInterval = 10; // Time between recorded values in seconds
unsigned long currMillis = 0;       // Timing variable
unsigned long prevMillis = 0;       // Timing variable
unsigned long prevRecordMillis = 0; // Timing variable
int scanCounter = 0;   // A variable to hold a count of scans
int recordCounter = 0; // A variable to hold a count of output records

//Declare sensor metric calculation varaibles
float HumSum; //Variable to hold sum of humidity measured over the record interval      
float HumAvg; //Variable to hold avg of humidity measured over the record interval
float TempSum; //Variable to hold sum of temp measured over the record interval
float TempAvg; //Variable to hold avg of temp measured over the record interval

void setup(){
  // Create a serial port and print header lines
  Serial.begin(9600);
  Serial.println("Temperature and Relative Humidity Sensor Output using a DHT22 Sensor");
  Serial.println("ScanNumber,ElapsedTime(us),Humidity,Temperature"); 

  // Set the pinMode on digital pin 10 to putput, check initialization and print header lines to SD card
  pinMode(10, OUTPUT); 
  if (!SD.begin(10)){
    Serial.println("SD card initialization failed!");
    return;
  }
  else{
   Serial.println("SD card initialization successful!");
  }
  File myFile = SD.open("hw1-2.txt", FILE_WRITE);
  myFile.println("RecordNumber,ElapsedTime(us),Humidity,Temperature");
  myFile.close();
  
  // Begin communication with the DHT sensor
  dht.begin();
}

void loop(){
  //Open txt file to write sensors variabes
  File myFile = SD.open("hw1-2.txt", FILE_WRITE);
  
  // Get the current time (number of microseconds since the program started)
  currMillis = millis();

  // Check timing to see if the scan interval has been reached
  if ((currMillis - prevMillis) >= (scanInterval * 1000))
  {
    // If YES, do a scan
    // -----------------  
    // Increment the scan counter variable
    scanCounter ++;  // The "++" operator adds 1 to a variable

    // Perform measurements and calculations here
    // Get the most recent measurements from the sensor
    float hum = dht.readHumidity();  // Get the humidity value in percent
    HumSum += hum;
    float degC = dht.readTemperature(); // Get the temperature value in celsius
    TempSum += degC;
    
    // Create a string with output for this scan to print to the serial port
    String stringToPrint = String(scanCounter) + "," + String(currMillis/1000) + "," + hum + "," + degC;
    Serial.println(stringToPrint);

    // Manage the timing variables to reflect that I just finished a scan
    prevMillis = currMillis;

    // Check to see if it's time to record data
    if ((currMillis - prevRecordMillis) >= (recordInterval * 1000))
    {
      HumAvg = HumSum / scanCounter;
      TempAvg = TempSum / scanCounter;
      // Increment the record counter
      recordCounter ++;
      
      // Create a string to record the output data to the serial port and write to sd card
      String recordToPrint = String(recordCounter) + "," + String(currMillis/1000) + "," + String(HumAvg) + "," + String(TempAvg);
      Serial.println(recordToPrint);
      myFile.println(recordToPrint);
      
      // Manage to timing variables to reflect that I just recorded data and reset the scanCounter and randomSum variables for the next scan
      prevRecordMillis = currMillis;
      scanCounter = 0;
      HumSum = 0;
      TempSum=0;
    }
  } 
  myFile.close();
}
