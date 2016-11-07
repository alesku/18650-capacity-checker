/* 
* Battery Capacity Checker, uses Nokia 5110 Display
* Uses 1 Ohm power resister as shunt - Load can be any suitable resister or lamp
* 
* YouTube Video: https://www.youtube.com/embed/qtws6VSIoYk
* http://AdamWelch.Uk
* 
* Required Library - LCD5110_Graph.h - http://www.rinkydinkelectronics.com/library.php?id=47
*/

#include "LCD5110_Graph.h"
LCD5110 myGLCD(5, 6, 7, 9, 8);  // Setup Nokia 5110 Screen SCLK/CLK=5, DIN/MOSI/DATA=6, DC/CS=7, RST=9 Chip Select/CE/SCE=8,
extern uint8_t SmallFont[];
extern uint8_t MediumNumbers[];

#define gatePin 10
#define highPin A0
#define lowPin A1

boolean finished = false;
int printStart = 0;
int interval = 5000;  //Interval (ms) between measurements

float mAh = 0.0;
float shuntRes = 1.0;  // In Ohms - Shunt resistor resistance
float voltRef = 4.71; // Reference voltage (probe your 5V pin) 

float current = 0.0;
float battVolt = 0.0;
float shuntVolt = 0.0;
float battLow = 2.9;

unsigned long previousMillis = 0;
unsigned long millisPassed = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Battery Capacity Checker v1.1");
  Serial.println("battVolt  current     mAh");
 
  digitalWrite(gatePin, LOW);
 
  myGLCD.InitLCD(); //initialize LCD with default contrast of 70
  myGLCD.setContrast(68);
  myGLCD.setFont(SmallFont); // Set default font size. tinyFont 4x6, smallFont 6x8, mediumNumber 12x16, bigNumbers 14x24
  myGLCD.clrScr();
  myGLCD.print("Battery",CENTER,0);
  myGLCD.print("Check",CENTER,12);
  myGLCD.print("Please Wait",CENTER,24);
  myGLCD.print("AdamWelch.Uk",8,40);
  myGLCD.update(); 
  delay(2000);
  myGLCD.clrScr();
}
 
void loop() {
  battVolt = analogRead(highPin) * voltRef / 1024.0;
  shuntVolt = analogRead(lowPin) * voltRef / 1024.0;
   
  if(battVolt >= battLow && finished == false){
      digitalWrite(gatePin, HIGH);
      millisPassed = millis() - previousMillis;
      current = (battVolt - shuntVolt) / shuntRes;
      mAh = mAh + (current * 1000.0) * (millisPassed / 3600000.0);
      previousMillis = millis();
 
      myGLCD.clrScr();
      myGLCD.print("Discharge",CENTER,0);
      myGLCD.print("Voltage:",0,10);
      myGLCD.printNumF(battVolt, 2,50,10);
      myGLCD.print("v",77,10);
      myGLCD.print("Current:",0,20);
      myGLCD.printNumF(current, 2,50,20);
      myGLCD.print("a",77,20);
      myGLCD.printNumI(mAh,30,30);
      myGLCD.print("mAh",65,30);
      myGLCD.print("Running",CENTER,40);
      myGLCD.update(); 
       
      Serial.print(battVolt);
      Serial.print("\t");
      Serial.print(current);
      Serial.print("\t");
      Serial.println(mAh);
       
      delay(interval);
  }
  
  if(battVolt < battLow){
      digitalWrite(gatePin, LOW);
      
      finished = true;
       
      if(mAh < 10) {
        printStart = 40;
      }
      else if(mAh < 100) {
        printStart = 30;
      }
      else if(mAh <1000) {
        printStart = 24;
      }
      else if(mAh <10000) {
        printStart = 14;
      }
      else {
        printStart = 0;
      }

      myGLCD.clrScr();
      myGLCD.print("Discharge",CENTER,0);
      myGLCD.print("Voltage:",0,10);
      myGLCD.printNumF(battVolt, 2,50,10);
      myGLCD.print("v",77,10);
      myGLCD.setFont(MediumNumbers);
      myGLCD.printNumI(mAh,printStart,21);
      myGLCD.setFont(SmallFont);
      myGLCD.print("mAh",65,30);
      myGLCD.print("Complete",CENTER,40);
      myGLCD.update(); 
      delay(interval * 2);
  }
}
