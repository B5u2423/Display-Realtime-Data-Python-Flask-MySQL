#include "DHT.h"
#include <WiFi.h>
#include <HTTPClient.h>

#define DHTPIN 19
#define DHTTYPE DHT11
// #define ONBOARD_LED 2

const char* ssid = "WiFi Name";
const char* password = "Wifi Password";
String SERVER = "http://<<domain iP>>:<<port>>/";

DHT dht(DHTPIN, DHTTYPE);

float temperature = 0;
float humidity = 0;

void setup() {
  Serial.begin(115200);
  dht.begin();
  connect_to_wifi();
}

void loop() {
  // reconnecting
  if (WiFi.status() != WL_CONNECTED) {
    connect_to_wifi();
  }
 
  delay(3000);
  get_sensor_data();
  String postData = "temperature=" + String(temperature) + "&humidity=" + String(humidity);

  HTTPClient http;
  http.begin(SERVER);

  int httpCode = http.POST(postData);
  http.addHeader("Content-Type", "application/x-www-urlencoded");
}

/*******************************/

void connect_to_wifi () {
  WiFi.mode(WIFI_OFF);
  delay(1000);

  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);
  Serial.println("Connecting!");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.printf("\n [O] Connected to: %s\n", ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP()); 
}

/*******************************/

void get_sensor_data () {
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("[X] Failed to read from DHT sensor!");
    temperature = 0;
    humidity = 0;
    return;
  }

  Serial.println(humidity);
  Serial.println(temperature);
}
