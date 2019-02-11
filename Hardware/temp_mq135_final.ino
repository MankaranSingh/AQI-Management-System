/*
make the connections without tx and rx first,then upload the code connect tx,rx and the reset arduino
Wiring - 
 LM35             Arduino
 Pin 1            5V
 Pin 2            A0
 Pin 3            GND
 
 ESP8266          Arduino
 CH_PD,VCC        3.3V
 GND              GND
 TX               RX (Arduino)
 RX               TX (Ardino)
 Written By
 Angelin John
 Last Update - 
 January 19, 2017
 
*/
#include "dht.h"
#include <LiquidCrystal.h>
#define dht_apin A1
int sensorValue;
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
dht DHT;
const int calibratingValue = 42;

int value=0;
float temp=0;

#define SSID "Radiant32" // type in your SSID
#define PASS "12345678" // type in your password
#define IP "192.168.43.161"//Thingspeak IP Address,need not be changed
String GET = "GET /32.53-42.54-Punjab-Patiala-PremNagar-79-54-7/Radiant32 HTTP/1.1\r\nHost: 192.168.43.161"; // instead of F51VSF3MUOE6UYHM, add the write API key of your channel.
int wifir=0;

void setup()
{
  Serial.begin(115200);
  lcd.begin(16, 2);//baud rate for ESP8266 and Serial Monitor
  Serial.println("AT");
  delay(5000);
  if(Serial.find("OK")){
    Serial.println("OK");
    connectWiFi();
    delay(1000);
  }
}

void loop(){
  
  //Get Temperature value and convert it to String
  DHT.read11(dht_apin);  
    sensorValue = analogRead(0); 
    sensorValue += calibratingValue;    
    delay(5000);
    
 
  //Upload temperature value to thingspeak.com api
  GET = "GET /32.53-42.54-Punjab-Patiala-PremNagar-"+String(sensorValue)+"-"+String(DHT.humidity)+"-"+String(DHT.temperature)+"/Radiant32 HTTP/1.1\r\nHost: 192.168.43.161";
  
  String cmd = "AT+CIPSTART=\"TCP\",\"";//set up TCP connection
  cmd += IP;
  cmd += "\",5000";
  Serial.println(cmd);
  delay(1000);
    if(Serial.find("Error")){
      Serial.println("AT+CIPSTART Error");
      return;
    }
 
  cmd = GET;
  cmd += "\r\n\r\n";
  Serial.print("AT+CIPSEND=");//send TCP/IP data
  Serial.println(cmd.length());
  delay(1000);
    if(Serial.find(">")){ 
      Serial.print(cmd); 
    }
    else
      Serial.println("AT+CIPSEND error");
  delay(16000); // Thingspeak can update the value only at an interval of 15 secs.
}


//Connect to WiFi when Arduino starts up. One time run called during void setup().
int connectWiFi(){
  Serial.println("AT+CWMODE=3");//wifi mode
  delay(2000);
  String cmd="AT+CWJAP=\"";//join access point
  cmd+=SSID;
  cmd+="\",\"";
  cmd+=PASS;
  cmd+="\"";
  Serial.println(cmd);
  delay(15000); //it takes some time to connect to WiFi and get an IP address
}
