// Define all the I/O
#define DHTPIN 2
#define DHTTYPE DHT11
#define RELAY_PIN 12 // Arduino pin connect to relay
#define SOIL_MOISTURE_PIN A0  // Analog pin connected to soil moisture sensor

// Include all the libraries
#include <Wire.h>
#include <i2cdetect.h>
#include "DHT.h"
#include <FastIO.h>
#include <I2CIO.h>
#include <LCD.h>
#include <LiquidCrystal.h>
#include <LiquidCrystal_I2C.h>
#include <LiquidCrystal_SR.h>
#include <LiquidCrystal_SR2W.h>
#include <LiquidCrystal_SR3W.h>
#include <OneWire.h>
#include <DallasTemperature.h>

//I2C pins declaration
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

// Declare 1-wire sensor pin
const int SENSOR_PIN = 13; // Arduino pin connected to DS18B20 sensor's DQ pin

// Temperature sensor
OneWire oneWire(SENSOR_PIN);         // setup a oneWire instance
DallasTemperature tempSensor(&oneWire); // pass oneWire to DallasTemperature library

DHT dht(DHTPIN, DHTTYPE);

// Variables to store sensor values
int soilMoistureValue = 0;
float humidity = 0.0;
float temperature = 0.0;

// Variables for float sensor
int FloatSensor = 4;   
int led = 13;     
int buzzer = 3;      
int buttonState = 1; //reads pushbutton status
float tempCelsius;    // temperature in Celsius

// Threshold values
int soilMoistureThreshold = 660; // Adjust this value based on calibration

void setup() {
  // Initialize serial communication
  Serial.begin(115200);

  // Initialize the DHT sensor
  dht.begin();

  // Initialize the Temperature sensor
  tempSensor.begin();    // initialize the sensor

  // Initialize the LCD 
  lcd.begin(16,2);//Defining 16 columns and 2 rows of lcd display
  lcd.backlight();//To Power ON the back light
  //lcd.backlight();// To Power OFF the back light

  // Setting pin mode for the Float sensor
  pinMode(FloatSensor, INPUT_PULLUP); //Arduino Internal Resistor 10K
  pinMode (led, OUTPUT);
  pinMode (buzzer, OUTPUT);

  // Setting pin mode for relay
  pinMode(RELAY_PIN, OUTPUT);

}

void loop() {
  // Delay to allow sensors to stabilize
  delay(1000);

  // Read soil moisture value
  soilMoistureValue = analogRead(SOIL_MOISTURE_PIN);

  // Check current soil moisture sensor value and compare against threshold
  if (soilMoistureValue > soilMoistureThreshold) {
    Serial.println("The soil is DRY => turn pump ON");
    digitalWrite(RELAY_PIN, LOW);
    delay(200);
  } else {
    Serial.println("The soil is WET => turn pump OFF");
    digitalWrite(RELAY_PIN, HIGH);
    delay(200);
  }

  // Read temperature and humidity values
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Read water temperature
  tempSensor.requestTemperatures();             // send the command to get temperatures
  tempCelsius = tempSensor.getTempCByIndex(0);  // read temperature in Celsius

  // Check if any reads failed and exit early (to try again)
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Check for float level
  buttonState = digitalRead(FloatSensor);
  if (buttonState == LOW) 
  { 
    digitalWrite(led, LOW);
    tone(buzzer, 10000,1000);
    Serial.println( "WATER LEVEL - LOW"); 
  } 
  else 
  { 
    digitalWrite(led, HIGH);
    //tone(buzzer, 10000,500);
    Serial.println( "WATER LEVEL - HIGH" ); 
  }

  // Send data to serial monitor
//  Serial.print("Soil Moisture: ");
//  Serial.println(soilMoistureValue);
//    
//  Serial.print("Water Temperature: ");
//  Serial.println(tempCelsius);    // print the temperature in Celsius

  // Send data to NodeMCU
  Serial.print(temperature);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.print(tempCelsius);
  Serial.print(",");
  Serial.println(soilMoistureValue);

  // Display readings on the LCD screen
  displayLCD("Soil Moisture:", String(soilMoistureValue));
  delay(2000);

  displayLCD("Humidity:", String(humidity) + "%");
  delay(2000);

  displayLCD("Room Temp:", String(temperature) + "C");
  delay(2000);

  displayLCD("Water Temp:", String(tempCelsius) + "C");
  delay(2000);

}

void displayLCD(String line1, String line2){
  lcd.clear();
  lcd.setCursor(0,0); 
  lcd.print(line1);
  lcd.setCursor(0,1); 
  lcd.print(line2);
  }
