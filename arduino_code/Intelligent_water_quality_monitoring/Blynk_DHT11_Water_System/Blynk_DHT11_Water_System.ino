#define BLYNK_TEMPLATE_ID "TMPL6nhHuSrPD"
#define BLYNK_TEMPLATE_NAME "Water Quality Monitoring System"
#define BLYNK_AUTH_TOKEN "KXGasdvmTt_Fugzj6B-OW15OEprMuJgQ"

// Libraries
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

// Blynk Auth Token
char auth[] = "KXGasdvmTt_Fugzj6B-OW15OEprMuJgQ";

// Your WiFi credentials
char ssid[] = "mzq_resources_2.4GHz";
char pass[] = "faizal_a";

//char ssid[] = "Deco1";
//char pass[] = "srinpek123";

BlynkTimer timer;

void setup() {
  // Debug console
  Serial.begin(115200);

  // Blynk setup
  Blynk.begin(auth, ssid, pass);

  // Setup a function to be called every 2 seconds
  timer.setInterval(2000L, sendSensorData);
}

void sendSensorData() {
  static String receivedData = "";
  while (Serial.available()) {
    char c = (char)Serial.read();
    receivedData += c;
    if (c == '\n') {
      // Remove any carriage returns and trim the data
      receivedData.trim();

      // Split the received data
      int firstCommaIndex = receivedData.indexOf(',');
      int secondCommaIndex = receivedData.indexOf(',', firstCommaIndex + 1);
      int thirdCommaIndex = receivedData.indexOf(',', secondCommaIndex + 1);

      if (firstCommaIndex != -1 && secondCommaIndex != -1 && thirdCommaIndex != -1) {
        // Extract air temperature
        String airTempStr = receivedData.substring(0, firstCommaIndex);
        float airTemp = airTempStr.toFloat();

        // Extract air humidity
        String airHumidityStr = receivedData.substring(firstCommaIndex + 1, secondCommaIndex);
        float airHumidity = airHumidityStr.toFloat();

        // Extract water temperature
        String waterTempStr = receivedData.substring(secondCommaIndex + 1, thirdCommaIndex);
        float waterTemp = waterTempStr.toFloat();

        // Extract turbidity
        String turbidityStr = receivedData.substring(thirdCommaIndex + 1);
        int turbidity = turbidityStr.toInt();

        // Debug prints
        Serial.print("Air Temperature: ");
        Serial.println(airTemp);
        Serial.print("Air Humidity: ");
        Serial.println(airHumidity);
        Serial.print("Water Temperature: ");
        Serial.println(waterTemp);
        Serial.print("Turbidity: ");
        Serial.println(turbidity);

        // Send data to Blynk app
        Blynk.virtualWrite(V5, airTemp);
        Blynk.virtualWrite(V6, airHumidity);
        Blynk.virtualWrite(V7, waterTemp);
        Blynk.virtualWrite(V8, turbidity);
      }

      // Clear received data
      receivedData = "";
    }
  }
}

void loop() {
  Blynk.run();
  timer.run();
}
