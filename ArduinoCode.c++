#include <DHT.h>

#define DHTPIN A0        // Pin connected to the DHT11 data pin
#define DHTTYPE DHT11   // DHT11 sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature(); // Celsius

  // If the reading failed, skip the rest of the loop
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Error: Failed to read from DHT11");
    delay(1000);
    return;
  }

  // Send the values in a simple format
  Serial.print(temperature);
  Serial.print(",");
  Serial.println(humidity);
  //delay(120000); // DHT11 can only be read every ~1–2 seconds
  delay(120000);
}
