//We always have to include the library
#include "LedControl.h"

/*
 Now we need a LedControl to work with.
 ***** These pin numbers will probably not work with your hardware *****
 pin 12 is connected to the DataIn 
 pin 11 is connected to the CLK 
 pin 10 is connected to LOAD 
 We have only a single MAX72XX.
 */
LedControl ledControl =LedControl(12,11,10,1);

/* we always wait a bit between updates of the display */
unsigned long delaytime=250;

void setup() {
  /*
   The MAX72XX is in power-saving mode on startup,
   we have to do a wakeup call
   */
  ledControl.shutdown(0,false);
  /* Set the brightness to a medium values */
  ledControl.setIntensity(0,8);
  /* and clear the display */
  ledControl.clearDisplay(0);
}


/*
 This method will display the characters for the
 word "Arduino" one after the other on digit 0. 
 */
void writeArduinoOn7Segment() {
    ledControl.setChar(0,0,'a',false);
  delay(delaytime);
  ledControl.setRow(0,0,0x05);
  delay(delaytime);
  ledControl.setChar(0,0,'d',false);
  delay(delaytime);
  ledControl.setRow(0,0,0x1c);
  delay(delaytime);
  ledControl.setRow(0,0,B00010000);
  delay(delaytime);
  ledControl.setRow(0,0,0x15);
  delay(delaytime);
  ledControl.setRow(0,0,0x1D);
  delay(delaytime);
  ledControl.clearDisplay(0);
  delay(delaytime);
} 

/*
  This method will scroll all the hexa-decimal
 numbers and letters on the display. You will need at least
 four 7-Segment digits. otherwise it won't really look that good.
 */
void scrollDigits() {
  for(int i=0;i<13;i++) {
      ledControl.setDigit(0,3,i,false);
      ledControl.setDigit(0,2,i+1,false);
      ledControl.setDigit(0,1,i+2,false);
      ledControl.setDigit(0,0,i+3,false);
    delay(delaytime);
  }
  ledControl.clearDisplay(0);
  delay(delaytime);
}

void loop() { 
  writeArduinoOn7Segment();
  scrollDigits();
}
