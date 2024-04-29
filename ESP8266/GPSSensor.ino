#include <ArduinoJson.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define BUTTON_PIN D7

TinyGPSPlus gps;
SoftwareSerial SerialGPS(4, 5); 

const char* ssid = "";
const char* password = "";
const char* url = "";
 
JsonDocument doc;
HTTPClient http;
WiFiClient client;

void setup(){
  Serial.begin(115200);
  SerialGPS.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.println();
  Serial.print("Connecting");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());
}

String generateRandomString(int length){
  String randomString = "";
  for (int i = 0; i < length; i++) {
    char randomChar = random('a', 'z' + 1);
    randomString += randomChar;
  } 
  return randomString;
}

String streetDamage(){
  String Damage[] = {"D00", "D10", "D20", "D40"};
  int number = random(0, 4);
  return Damage[number];   
 }

void loop(){
   while (SerialGPS.available() > 0) {
    if (gps.encode(SerialGPS.read())){
      if (gps.location.isValid()) {
        float Latitude = gps.location.lat();
        float Longitude = gps.location.lng();
        String LatitudeString = String(Latitude , 6);
        String LongitudeString = String(Longitude , 6);
        int button_state = digitalRead(BUTTON_PIN);
        if (button_state == LOW){
          doc["lat"] = LatitudeString;
          doc["long"] = LongitudeString;
          doc["imagename"] = generateRandomString(8) + ".png";
          doc["damage"] = streetDamage();
          http.begin(client, url);
          String requestBody;
          serializeJson(doc, requestBody);
          int httpResponseCode = http.POST(requestBody);
          http.end();
          delay(1000);
        }
      }
    }
   } 
}
