
#pragma once

#include "utility.h"

struct JoyStick
{
    struct PinLayout
    {
        int analogXPin;
        int analogYPin;
        int buttonClickPin;
    };

    struct Listener
    {
        virtual void joyStickUpdate (JoyStick&, Direction) = 0;
        virtual void joyStickButtonDown (JoyStick&) {}
    };


    explicit JoyStick (const PinLayout& layout) : pinLayout (layout) {}


    void setup() const
    {
        pinMode (pinLayout.analogXPin, INPUT);
        pinMode (pinLayout.analogYPin, INPUT);
        pinMode (pinLayout.buttonClickPin, INPUT);
    }


    void update()
    {
        if (listener == nullptr)
            return;

        auto d = direction;

        constexpr auto halfRes = resolution / 2;

        auto xVal = analogRead (pinLayout.analogXPin);
        auto yVal = analogRead (pinLayout.analogYPin);
        auto buttonDown = (bool) digitalRead (pinLayout.buttonClickPin);

        auto absX = abs (xVal - halfRes);
        auto absY = abs (yVal - halfRes);

        if (absX > threshold || absY > threshold)
        {
            if (absY > absX)
                d = yVal <= halfRes ? Direction::up : Direction::down;
            else
                d = xVal <= halfRes ? Direction::right : Direction::left;
        }

        if (d != direction)
            listener->joyStickUpdate (*this, direction = d);

        if (buttonDown == 0)
            listener->joyStickButtonDown (*this);

        Serial.println("update js");
    }


    void setListener (Listener* l)
    {
        listener = l;
    }

private:
    const PinLayout pinLayout;
    Listener* listener = nullptr;
    static constexpr auto resolution = 1024;
    static constexpr auto threshold = 400;
    Direction direction = Direction::down;
};