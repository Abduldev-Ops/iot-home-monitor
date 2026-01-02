#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11
#define PIRPIN 7

DHT dht(DHTPIN, DHTTYPE);
bool motionDetected = false;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(PIRPIN, INPUT);
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int motion = digitalRead(PIRPIN);

  if (motion == HIGH) {
    motionDetected = true;
  } else {
    motionDetected = false;
  }

  // Send data to Python
  Serial.print(t);
  Serial.print(",");
  Serial.print(h);
  Serial.print(",");
  Serial.println(motionDetected ? "1" : "0");

  delay(200);
}
