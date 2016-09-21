/*
Measurement Example Usig the DHT22 Sensor
Test sketch to demonstrate how to make sensor measurements
Created By:  Jeff Horsburgh
Creation Date: 8/13/2016
Sensor Wiring (AM302 Wired DHT22 Sensor):
Red    --> +5V
Black  --> Ground
Yellow --> Digital port 2
*/
// Include the DHT sensor library
#include "DHT.h"

// Define the digital pin you are connecting the DHT sensor to
#define DHTPin 2 

// The DHT library supports multiple DHT sensors, so need to 
// define the type of sensor we are using
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

// Initialize DHT sensor using the pin and sensor type
DHT dht(DHTPin, DHTTYPE);

void setup() {
  // Open a serial port so we can watch the output of the sensor
  Serial.begin(9600);
  Serial.println("Temperature and Relative Humidity Sensor Output");
  Serial.println("Measurements using a DHT22 Sensor");

  // Begin communication with the DHT sensor
  dht.begin();
}

void loop() {
  // Delay for 2 seconds before a measurement
  // Reading the values of temperature or humidity takes up to 2 seconds
  // So put a 2 second delay at the beginning of the loop 
  delay(2000); // delay in ms
  
  // Get the most recent measurements from the sensor
  float hum = dht.readHumidity();  // Get the humidity value in percent
  float degC = dht.readTemperature(); // Get the temperature value in Celisius

  // The sensor will also return the temperature as Fahrenheit (isFahrenheit = true)
  float degF = dht.readTemperature(true);

  // Check to see if any reads failed and exit the loop early to try again
  // "||" is the Arduino Boolean "OR" operator
  if (isnan(hum) || isnan(degC) || isnan(degF)) {
    Serial.println("Failed to read from DHT sensor!");
    return; // This exits the main loop and starts the next iteration
  }

  // Print the sensor output to the serial port
  Serial.print("Humidity: ");
  Serial.print(hum);
  Serial.print(" %\t"); // Print a tab character
  Serial.print("Temperature: ");
  Serial.print(degF);
  Serial.println(" *F"); // Do a println on the last part of the string so it adds a new line
}
