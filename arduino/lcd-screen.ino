#include <Wire.h> // Library for I2C communication
#include <LiquidCrystal_I2C.h> // Library for LCD
#include <Firmata.h>
LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2);

int lastLine = 1;

void setup() {
  lcd.init();
  lcd.backlight();
  Firmata.setFirmwareVersion( FIRMATA_MAJOR_VERSION, FIRMATA_MINOR_VERSION );
  Firmata.attach( STRING_DATA, stringDataCallback);
  Firmata.begin();  
}

void stringDataCallback(char *stringData){
   if ( lastLine ) {
     lastLine = 0;
     lcd.clear();
   } else {
     lastLine = 1;
     lcd.setCursor(0,1);
   }
   lcd.print(stringData);
}


void loop() {
  lcd.setCursor(2, 0); 
  while ( Firmata.available() ) {
    Firmata.processInput();
  }
}