
#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
float randNumber1;
float randNumber2;

// Set these to run example.
#define FIREBASE_HOST "mydata-b959c-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "v4gY575tOTE3x1D5kEhyN3rU6ER7CalD4kLBUBKk"
#define WIFI_SSID "MAHMOUD"
#define WIFI_PASSWORD "11111111"

void setup() {
  Serial.begin(9600);

  // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  
  //////////////////
// set value
  //String st=Firebase.pushInt("number",22);
  //Serial.println(st);
  
  }

void loop() {
 randNumber1 = random(50);
 randNumber2 = random(50);
Firebase.setFloat("v1", randNumber1);
Firebase.setFloat("v2", randNumber2);
  // handle error
  if (Firebase.failed()) {
      Serial.println(Firebase.error());
      Serial.print("setting /number failed:");
        
      return;}
  delay(1500);
  
  
}
