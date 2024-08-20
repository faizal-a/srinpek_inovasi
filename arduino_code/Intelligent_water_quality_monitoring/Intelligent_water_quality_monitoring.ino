#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <LiquidCrystal.h>
#include <LiquidCrystal_I2C.h>

// Pin definitions
#define DHTPIN 2
#define DHTTYPE DHT11
#define TURBIDITY_PIN A0
#define WATER_TEMP_PIN 4
#define BUZZER_PIN 3
#define LED_PIN 11

// Initialize sensors and LCD
DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(WATER_TEMP_PIN);
DallasTemperature waterTempSensor(&oneWire);
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

void setup() {
  // Initialize Serial for ESP8266 communication
  Serial.begin(115200);

  // Initialize sensors
  dht.begin();
  waterTempSensor.begin();

  // Initialize LCD
  lcd.begin(16, 2);

  // Setup pins
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // Read sensors
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  waterTempSensor.requestTemperatures();
  float waterTemp = waterTempSensor.getTempCByIndex(0);
  int turbidityValue = analogRead(TURBIDITY_PIN);

  // Display data on LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Water Temp: " + String(waterTemp) + "C");
  lcd.setCursor(0, 1);
  lcd.print("Turbidity: " + String(turbidityValue));

  // Prepare data to send
  String data = String(waterTemp) + "," + String(t) + "," + String(h) + "," + String(turbidityValue) + "\n";

  // Send data to ESP8266
//  Serial.print(data);

  // Trigger buzzer and LED if turbidity is high
  if (turbidityValue < 830) { // Example threshold
    digitalWrite(BUZZER_PIN, HIGH);
    digitalWrite(LED_PIN, HIGH);
    tone(BUZZER_PIN, 10000,2000);
  } else {
    digitalWrite(BUZZER_PIN, LOW);
    digitalWrite(LED_PIN, LOW);
  }

    // Send data to ESP8266
  Serial.print(t); Serial.print(",");
  Serial.print(h); Serial.print(",");
  Serial.print(waterTemp); Serial.print(",");
  Serial.println(turbidityValue);

  delay(2000); // Delay for readability
}
