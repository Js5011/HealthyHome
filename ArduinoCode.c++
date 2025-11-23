#include <DHT.h>
#include <LiquidCrystal.h>

// DHT11 Setup
#define DHTPIN A0        // Pin connected to the DHT11 data pin
#define DHTTYPE DHT11    // DHT11 sensor
DHT dht(DHTPIN, DHTTYPE);

// LCD Setup (RS, E, D4, D5, D6, D7)
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup() {
  Serial.begin(9600);
  dht.begin();

  // LCD Init
  lcd.begin(16, 2);
  lcd.print("Initializing...");
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature(); // Celsius

  // If the reading failed, skip the rest of the loop
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Error: Failed to read from DHT11");

    lcd.clear();
    lcd.print("Read Error");

    delay(1000);
    return;
  }

  // Send the values in a simple format (unchanged)
  Serial.print(temperature);
  Serial.print(",");
  Serial.println(humidity);

  // LCD Output
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temperature);
  lcd.print(" C");

  lcd.setCursor(0, 1);
  lcd.print("Humidity: ");
  lcd.print(humidity);
  lcd.print("%");

  delay(600000); // unchanged
}
