#include <SPI.h>
#include <WiFi.h>
#include <Wire.h>
#include <WifiLocation.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <SD.h>
#include "time.h"
#include "DHT.h"
#include "Adafruit_VEML6070.h"

#define LED1_PIN 12   
// sd card cs pin GPIO5
#define CS_PIN 5
#define DHT_PIN 17           
#define DHT_TYPE DHT21
#define VEML6070_ON_PIN 16  

#define API_KEY "API_KEY"

const char* FIREBASE_DATABASE = "https://url.firebaseio.com";
const char* FIREBASE_APIKEY   = "FIREBASE_APIKEY";
const char* FIREBASE_EMAIL    = "USER@MAIL.COM";
const char* FIREBASE_PASSWORD = "user_password";

DHT dht(DHT_PIN, DHT_TYPE);
 
File archivo;

Adafruit_VEML6070 uv = Adafruit_VEML6070();

String lat = "";
String lon = ""; 
 
char ssid[32] = "XXXXXXXXXXXXX";
char password[32] = "12345678";

boolean isConnected = false;
int conAttempts = 0;
int maxConAttempts = 25;
int tryConnection = 0;

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec =  -5 * 3600;
const int   daylightOffset_sec = 0;


hw_timer_t * timer = NULL; /* create a hardware timer */

int MEASUREMENT_INTERVAL = 30; // 30 segundos

const char* fileName;
boolean withWifi = false;
String nodeName = "default";
String token = "";

WifiLocation location(API_KEY);

/**
 * PRENDE Y APAGA UN LED
 */
void IRAM_ATTR onTimer(){
  digitalWrite(LED1_PIN, !digitalRead(LED1_PIN));
}

/**
 * Escribe datos en la sd card para guardar información
 */
void writeFile(const char * path, String message){
  archivo = SD.open(path, FILE_APPEND);
  if (archivo) {
    String messageLn = message + "\n";
    const char* messageCStr = messageLn.c_str();
    size_t mensajeLength = strlen(messageCStr);
    archivo.write((const uint8_t*)messageCStr, mensajeLength);
    archivo.close();
  }
}

/**
 * Metodo para obtener la hora actual
 */
String printLocalTime(){
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    return "";
  }
  char dateTimeStr[20];
  snprintf(dateTimeStr, sizeof(dateTimeStr), "%02d:%02d:%02d",
           timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec);
  return String(dateTimeStr);
}

/**
 * Metodo para pbtener la fecha actual
 */
String printLocalDate(){
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    return "";
  }
  char dateTimeStr[20];
  snprintf(dateTimeStr, sizeof(dateTimeStr), "%02d-%02d-%02d",
           timeinfo.tm_mday, timeinfo.tm_mon + 1, timeinfo.tm_year % 100);
  return String(dateTimeStr);
}

/**
 * Metodo para guardar datos de la variable del sensor en el archivo
 */
void saveDataLog(float temp, float hum, float hif, float lux, String lat, String lon){
  String fileName = "/data_" + printLocalDate() + ".csv";
  const char* fileNameCStr = fileName.c_str();
  char dataStr[60];
  String hora = printLocalTime();
  snprintf(dataStr, sizeof(dataStr), "%s,%0.2f,%0.2f,%0.2f,%0.2f,%s,%s", hora, temp, hum, hif, lux, lat, lon);
  writeFile(fileNameCStr, String(dataStr));
}

String firebaseAuth(const char* femail, const char* fpassword, const char* fapikey) {
  HTTPClient http;
  String url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + String(fapikey);
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(30000); 

  String jsonPayload = "{\"email\":\"" + String(femail) + "\",\"password\":\"" + String(fpassword) + "\",\"returnSecureToken\":true}";
  
  int httpCode = http.POST(jsonPayload);

  // Check the response code
  if (httpCode == HTTP_CODE_OK) {
    DynamicJsonDocument response(1024);
    deserializeJson(response, http.getString());
    String idToken = response["idToken"];
    http.end();
    return idToken;
  } else {
    http.end();
    WiFi.disconnect(true);
    WiFi.mode(WIFI_OFF);
    connectToWiFi();
    return "";
  }
}

void intents() {
  tryConnection++;
  if (tryConnection >= 5) {
    ESP.restart();
  }
}

boolean firebaseSendData(const char* fdatabase, String token, String nodeName, String dateTime, String hum, String light, String lat, String lon, String temp) {
  HTTPClient http;
  String url = String(fdatabase)+ "/nodes/" + nodeName + ".json?auth=" + String(token);
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(30000); 
  String jsonPayload = "{\"dateTime\":\"" + dateTime + "\",\"hum\":" + hum + ",\"light\":" + light + ",\"location\":{\"lat\":" + lat + ",\"lng\":" + lon + "},\"temp\":" + temp + "}";
  
  int httpCode = http.PUT(jsonPayload);

  // Check the response code
  if (httpCode == HTTP_CODE_OK) {
    http.end();
    return true;
  } else {
    http.end();
    WiFi.disconnect(true);
    WiFi.mode(WIFI_OFF);
    connectToWiFi();
    return false;
  }
}

void connectToWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  int conAttempts = 0;
  while (WiFi.status() != WL_CONNECTED && conAttempts <= maxConAttempts) {
    delay(250);
    conAttempts++;
  }
  isConnected = (WiFi.status() == WL_CONNECTED);
  conAttempts = 0;
}

void initializeSDCard() {
  if (!SD.begin(CS_PIN)) return;
  
  File configFile = SD.open("/connection.txt");
  if (configFile) {
    String swithWifi = configFile.readStringUntil('\n');
    swithWifi.trim();
    withWifi = (swithWifi == "true" || swithWifi == "1");
    String sdelaySleep = configFile.readStringUntil('\n');
    sdelaySleep.trim();
    int delaySleepMinutes = sdelaySleep.toInt();
    MEASUREMENT_INTERVAL = delaySleepMinutes * 60;
    nodeName = configFile.readStringUntil('\n');
    nodeName.trim();
    String sssid = configFile.readStringUntil('\n');
    sssid.trim();
    sssid.toCharArray(ssid, sizeof(ssid));
    String spassword = configFile.readStringUntil('\n');
    spassword.trim();
    spassword.toCharArray(password, sizeof(password));
    configFile.close();
  }
}

void setup() {    
  //Serial.begin(115200);
  pinMode(LED1_PIN, OUTPUT);
  digitalWrite(LED1_PIN, HIGH);
  pinMode(VEML6070_ON_PIN, OUTPUT);  
  digitalWrite(VEML6070_ON_PIN, HIGH);

  dht.begin();
  uv.begin(VEML6070_1_T);
  Wire.begin();

  //LED WITHOUTH DELAY  
  timer = timerBegin(8000000);
  timerAttachInterrupt(timer, &onTimer);
  timerAlarm(timer, 500000, true, 0);
 
  initializeSDCard();

    
  if (withWifi) {
    connectToWiFi();
    while (token == "") token = firebaseAuth(FIREBASE_EMAIL, FIREBASE_PASSWORD, FIREBASE_APIKEY);

    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer, "time.nist.gov");
    delay(250);
    String localTime = printLocalTime();
  
    while (printLocalTime() == "") {
      //Serial.println("No se obtuvo fecha");
      WiFi.disconnect(true);
      connectToWiFi();
      configTime(gmtOffset_sec, daylightOffset_sec, ntpServer, "time.nist.gov");
      delay(250);
    }
    delay(250);
    
    location_t loc = location.getGeoFromWiFi();
    location.getSurroundingWiFiJson();
    lat = String(loc.lat, 7);
    lon = String(loc.lon, 7);
    while (lat.startsWith("0.00")) {
      intents();
      delay(125);
      location_t loc = location.getGeoFromWiFi();
      location.getSurroundingWiFiJson();
      lat = String(loc.lat, 7);
      lon = String(loc.lon, 7);
    }
   
    delay(250);
  } else {
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer, "time.nist.gov");
    delay(250);
  }

  //seet sleep timer wakeup
  esp_sleep_enable_timer_wakeup(MEASUREMENT_INTERVAL * 1000000);

  float hum = dht.readHumidity();
  float temp= dht.readTemperature();
  float hif = dht.computeHeatIndex(temp, hum, false);
  float light = uv.readUV();
  //SAVE DATA ON SD CARD
  saveDataLog(temp, hum, hif, light, lat, lon);
  String localDateTime = printLocalDate()  + " " + printLocalTime();

  if (withWifi) {
    //Disconnect
    WiFi.disconnect(true);
    WiFi.mode(WIFI_OFF);
    connectToWiFi();
    boolean result = false;
    while (!result) result = firebaseSendData(FIREBASE_DATABASE, token, nodeName, localDateTime, String(hum, 2), String(light, 2), lat, lon, String(temp, 2));
    delay(100);
    WiFi.disconnect(true);
    WiFi.mode(WIFI_OFF);
  }
  timerEnd(timer);
  esp_deep_sleep_start();
}

void loop() {}