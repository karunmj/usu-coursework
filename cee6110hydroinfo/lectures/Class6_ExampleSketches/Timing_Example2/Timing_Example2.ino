/*
Timing Example 2
Test sketch to demonstrate how the timing functions work
Created By:  Jeff Horsburgh
Creation Date: 8/13/2016
*/

// Declare some needed variables
int scanInterval = 1;   // Time between scans within the main loop in seconds
int recordInterval = 10; // Time between recorded values in seconds
unsigned long currMicros = 0;       // Timing variable
unsigned long prevMicros = 0;       // Timing variable
unsigned long prevRecordMicros = 0; // Timing variable
int scanCounter = 0;   // A variable to hold a count of scans
int recordCounter = 0; // A variable to hold a count of output records
float randomNum;       // Variable to hold a random number
float randomSum;       // Variable to enable calculation of the average value for randNum
float avgRandomNum;    // Variable to hold the average value of randNum

void setup(){
  // Create a serial port and print a header line
  Serial.begin(9600);
  Serial.println("Timing Example 2 Sketch Output"); // Write a header line to the output
  Serial.println("ScanNumber, RandomNumber"); // Write column headers to output table
}

void loop(){
  // Get the current time 
  // (number of microseconds since the program started)
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
    randomNum = random(1, 10);  // Create a random number between 1 and 10
    randomSum += randomNum;     // Add the current random number to a sum
    
    // Create a string with output for this scan to print to the serial port
    // Use the "+" operator to concatenate strings together
    // The "String()" function converts numbers to strings
    String stringToPrint = String(scanCounter) + ", " + String(randomNum);
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
      avgRandomNum = randomSum / scanCounter;

      // Increment the record counter
      recordCounter ++;
      
      // Create a string to record the output data to the serial port
      String recordToPrint = "RecordNumber = " + String(recordCounter) + \
                             ", ElapsedTime (us) = " + String(currMicros) + \
                             ", Random Number Average = " + String(avgRandomNum);
      Serial.println(recordToPrint);
      
      // Manage to timing variables to reflect that I just recorded data
      // and reset the scanCounter and randomSum variables for the next scan
      prevRecordMicros = currMicros;
      scanCounter = 0;
      randomSum = 0;
    }
  } 
}
