#include <Arduino.h>

/*

constexpr auto joyStickXPin = A0;
constexpr auto joyStickYPin = A1;
constexpr auto joyStickButton = 2;


void setup()
{
    pinMode (joyStickButton, INPUT);
    pinMode (joyStickXPin, INPUT);
    pinMode (joyStickYPin, INPUT);
    digitalWrite(joyStickButton, HIGH);
    Serial.begin (9600);
}


void loop()
{
    auto joyStickXValue = analogRead (joyStickXPin);
    auto joyStickYValue = analogRead (joyStickYPin);
    auto joyStickButtonDown = digitalRead (joyStickButton);

    Serial.print ("x: ");
    Serial.print (joyStickXValue);
    Serial.print (", y: ");
    Serial.print (joyStickYValue);
    Serial.print (", button: ");
    Serial.println (joyStickButtonDown);

    delay (500);
}
 */

#include <LedControl.h>


/*
 Now we need a LedControl to work with.
 ***** These pin numbers will probably not work with your hardware *****
 pin 12 is connected to the DataIn
 pin 11 is connected to the CLK
 pin 10 is connected to LOAD
 ***** Please set the number of devices you have *****
 But the maximum default of 8 MAX72XX wil also work.
 */
LedControl lc = LedControl (12, 11, 10, 4);

/* we always wait a bit between updates of the display */
unsigned long delaytime = 500;

/*
 This time we have more than one device.
 But all of them have to be initialized
 individually.
 */
/*
void setup()
{
    //we have already set the number of devices when we created the LedControl
    int devices = lc.getDeviceCount();
    //we have to init all devices in a loop
    for (int address = 0; address < devices; address++)
    {
        lc.shutdown (address, false);
        lc.setIntensity (address, 8);
        lc.clearDisplay (address);
    }
}
*/
/*
void loop()
{
    //read the number cascaded devices
    int devices = lc.getDeviceCount();

    for (auto d = 0; d < devices; ++d)
        for (int row = 0; row < 8; row++)
        {
            lc.setColumn (d, row, 2);
            delay (500);
            lc.clearDisplay (d);
        }
}
 */

//constexpr auto joyStick2XPin = A3;
//constexpr auto joyStick2YPin = A4;
//constexpr auto joyStick2ButtonPin = 4;

constexpr auto joyStick2XPin = A5;
constexpr auto joyStick2YPin = A6;
constexpr auto joyStick2ButtonPin = 2;

constexpr auto joyStickXPin = A0;
constexpr auto joyStickYPin = A1;
constexpr auto joyStickButton = 2;


struct SequencerDisplay
{
    static constexpr int numDisplays = 4;
    static constexpr int numRows = 8;
    static constexpr int numColumnsPerHardwareDisplay = 8;
    static constexpr int numSequencerColumns = 32;

    template <typename Functor>
    void forEachPixel (Functor&& callback)
    {
        for (auto row = 0; row < numRows; ++row)
            for (auto column = 0; column < numColumnsPerHardwareDisplay * numDisplays; ++column)
                callback (*this, displayBuffer[row][column]);
    }

    void setup()
    {
        for (int display = 0; display < numDisplays; display++)
        {
            ledController.shutdown (display, false);
            ledController.setIntensity (display, 8);
            ledController.clearDisplay (display);
        }
    }

    void render()
    {
        clearScreen();

        for (auto row = 0; row < numRows; ++row)
        {
            for (auto display = 0; display < ledController.getDeviceCount(); ++display)
            {
                for (auto column = 0; column < numColumnsPerHardwareDisplay; ++column)
                {
                    auto col = column + display * numColumnsPerHardwareDisplay;
                    auto value = displayBuffer[row][col];
                    ledController.setLed (display, row, 7-column, value);
                }
            }
        }
    }

    // clears the hardware screen, leaves display buffer untouched
    void clearScreen()
    {
        for (auto display = 0; display < numDisplays; ++display)
            ledController.clearDisplay (display);
    }

    // this addressing works row[0-8], column[0-32]
    void turnLedOn (int row, int column)
    {
        displayBuffer[row][column] = true;
    }

    void turnLedOff (int row, int column)
    {
        displayBuffer[row][column] = false;
    }

    void turnRowOff (int row)
    {
        for (auto c = 0; c < numSequencerColumns; ++c)
            turnLedOff (row, c);
    }

    void turnColumnOff (int col)
    {
        for (auto r = 0; r < numRows; ++r)
            turnLedOff (r, col);
    }

    int displayBuffer[numRows][numColumnsPerHardwareDisplay * numDisplays] = {};
    LedControl ledController { 12, 11, 10, numDisplays };
};


SequencerDisplay display;

void setup()
{
    pinMode (joyStick2ButtonPin, INPUT);
    pinMode (joyStick2XPin, INPUT);
    pinMode (joyStick2YPin, INPUT);
    digitalWrite (joyStick2ButtonPin, HIGH);
    display.setup();
    Serial.begin (9600);
}


void loop()
{
    auto joyStickXValue = analogRead (joyStick2XPin);
    auto joyStickYValue = analogRead (joyStick2YPin);
    auto joyStickButtonDown = digitalRead (joyStick2ButtonPin);

    Serial.print ("x: ");
    Serial.print (joyStickXValue);
    Serial.print (", y: ");
    Serial.print (joyStickYValue);
    Serial.print (", button: ");
    Serial.println (joyStickButtonDown);

    for (auto c = 0; c < display.numSequencerColumns; ++c)
    {
        for (auto i = 0; i < 8; ++i)
        {
            display.turnLedOn (i, c);
            display.render();
            delay (10);
        }
        display.turnColumnOff (c);
    }


    //delay (500);
}