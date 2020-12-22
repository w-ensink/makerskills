#include <Arduino.h>


constexpr auto joyStickXPin = A0;
constexpr auto joyStickYPin = A1;
constexpr auto joyStickButton = 1;


void setup()
{
    pinMode (joyStickButton, INPUT);
    pinMode (joyStickXPin, INPUT);
    pinMode (joyStickYPin, INPUT);
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