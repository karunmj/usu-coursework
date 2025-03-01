/*
Data logger programming and data collection
CEE6110 Assignment#2
Karun Joseph, A02240287
*/

// Include DHT sensor, SD library
#include <DHT.h>
#include <SD.h>
#include <TimeLib.h>

#define TIME_HEADER  "T"   // Header tag for serial time sync message
#define TIME_REQUEST  7    // ASCII bell character requests a time sync message 


// Define DHT sensor digital pin to 2
#define DHTPin 2 

// Define type of DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

// Initialize DHT sensor using pin and sensor type
DHT dht(DHTPin, DHTTYPE);



int scanInterval = 5;   // Time between scans within the main loop in seconds
int recordInterval = 10; // Time between recorded values in seconds
unsigned long currMicros = 0;       // Timing variable
unsigned long prevMicros = 0;       // Timing variable
unsigned long prevRecordMicros = 0; // Timing variable
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
  File myFile = SD.open("hw1-1.txt", FILE_WRITE);
  myFile.println("RecordNumber,ElapsedTime(us),Humidity,Temperature");
  myFile.close();
  
  // Begin communication with the DHT sensor
  dht.begin();

  setSyncProvider( requestSync);  //set function to call when sync required
}

void loop(){
  if (Serial.available()) {
    processSyncMessage();
    
  }
  if (timeStatus()!= timeNotSet) {
    String comptime = String(hour())+":"+String(minute())+":"+String(second());
  }
  
  //Open txt file to write sensors variabes
  File myFile = SD.open("hw1-1.txt", FILE_WRITE);
  
  // Get the current time (number of microseconds since the program started)
  currMicros = micros();

  // Check timing to see if the scan interval has been reached
  if ((currMicros - prevMicros) >= (scanInterval * 1000000))
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
    String stringToPrint = String(scanCounter) + "," + String(currMicros) + "," + hum + "," + degC;
    Serial.println(stringToPrint);

    // Manage the timing variables to reflect that I just finished a scan
    prevMicros = currMicros;

    // Check to see if it's time to record data
    if ((currMicros - prevRecordMicros) >= (recordInterval * 1000000))
    {
      HumAvg = HumSum / scanCounter;
      TempAvg = TempSum / scanCounter;
      // Increment the record counter
      recordCounter ++;
      
      // Create a string to record the output data to the serial port and write to sd card
      String recordToPrint = String(recordCounter) + "," + String(currMicros) + "," + comptime + "," + String(HumAvg) + "," + String(TempAvg);
      Serial.println(recordToPrint);
      myFile.println(recordToPrint);
      
      // Manage to timing variables to reflect that I just recorded data and reset the scanCounter and randomSum variables for the next scan
      prevRecordMicros = currMicros;
      scanCounter = 0;
      HumSum = 0;
      TempSum=0;
    }
  } 
  myFile.close();
}

void processSyncMessage() {
  unsigned long pctime;
  const unsigned long DEFAULT_TIME = 1357041600; // Jan 1 2013

  if(Serial.find(TIME_HEADER)) {
     pctime = Serial.parseInt();
     if( pctime >= DEFAULT_TIME) { // check the integer is a valid time (greater than Jan 1 2013)
       setTime(pctime); // Sync Arduino clock to the time received on the serial port
     }
  }
}

time_t requestSync()
{
  Serial.write(TIME_REQUEST);  
  return 0; // the time will be sent later in response to serial mesg
}


