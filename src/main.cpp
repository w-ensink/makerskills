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

/* we always wait a bit between updates of the display */

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
/*
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
                    ledController.setLed (display, row, 7 - column, value);
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

    void turnColumnOn (int col)
    {
        for (auto r = 0; r < numRows; ++r)
            turnLedOn (r, col);
    }

    void turnRowOn (int row)
    {
        for (auto c = 0; c < numSequencerColumns; ++c)
            turnLedOn (row, c);
    }

    void turnOff()
    {
        for (auto row = 0; row < numRows; ++row)
            for (auto c = 0; c < numSequencerColumns; ++c)
                displayBuffer[row][c] = false;
    }

    bool displayBuffer[numRows][numColumnsPerHardwareDisplay * numDisplays] = {};
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
            delay (5);
        }
        display.turnColumnOff(c);
    }

    //display.turnOff();
   // display.render();

    //delay (500);
}
 */

//We always have to include the library

constexpr auto dataInPin = 12;
constexpr auto clkPin = 11;
constexpr auto loadPin = 10;
constexpr auto numDisplays = 8;

auto ledControl = LedControl { dataInPin, clkPin, loadPin, numDisplays };

unsigned long delaytime = 500;

// =====================================================================================

struct JoyStick
{
    struct PinLayout
    {
        int analogXPin;
        int analogYPin;
        int buttonClickPin;
    };

    enum struct Direction
    {
        left,
        right,
        up,
        down
    };

    struct Listener
    {
        virtual void joyStickUpdate (JoyStick&, Direction) = 0;
    };

    explicit JoyStick (const PinLayout& layout) : pinLayout (layout)
    {
    }

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

        constexpr auto halfRes = resolution / 2;

        auto xVal = analogRead (pinLayout.analogXPin);
        auto yVal = analogRead (pinLayout.analogYPin);
        auto buttonDown = (bool) digitalRead (pinLayout.buttonClickPin);

        auto absX = abs (xVal - halfRes);
        auto absY = abs (xVal - halfRes);

        if (absX > threshold)
        {
            if (absY > absX)
                direction = yVal > halfRes ? Direction::up : Direction::down;
            else
                direction = xVal > halfRes ? Direction::right : Direction::left;
        }

        listener->joyStickUpdate (*this, direction);
    }

    const PinLayout pinLayout;
    Listener* listener = nullptr;
    static constexpr auto resolution = 1024;
    static constexpr auto threshold = 400;
    Direction direction = Direction::down;
};

// =====================================================================================

// the display is like one long display of 8x64 broken in two
//
struct Display_16x32
{
    struct Spec
    {
        int dataInPin;
        int clkPin;
        int loadPin;
        int numDisplays;
    };

    struct Pixel
    {
        int x;
        int y;
    };

    explicit Display_16x32 (const Spec& spec) : spec (spec) {}

    void setup()
    {
        for (int display = 0; display < spec.numDisplays; display++)
        {
            ledController.shutdown (display, false);
            ledController.setIntensity (display, 8);
            ledController.clearDisplay (display);
        }
    }

    void turnOnPixel (const Pixel& pixel) noexcept
    {
        setStateOfPixel (pixel, true);
    }

    void turnOffPixel (const Pixel& pixel) noexcept
    {
        setStateOfPixel (pixel, false);
    }

private:
    Spec spec;

    LedControl ledController {
        spec.dataInPin,
        spec.clkPin,
        spec.loadPin,
        spec.numDisplays
    };

    void setStateOfPixel (const Pixel& pixel, bool state)
    {
        auto x = 7 - (pixel.x % 8);  //+ 32 * (pixel.x >= 32);
        auto y = 7 - (pixel.y % 8);
        auto display = (pixel.y / 8) + (pixel.x / 8) * 4;
        ledController.setLed (display, x, y, state);
    }
};

// =====================================================================================

const auto displaySpec = Display_16x32::Spec {
    .dataInPin = dataInPin,
    .clkPin = clkPin,
    .loadPin = loadPin,
    .numDisplays = numDisplays
};

auto display = Display_16x32 { displaySpec };

void setup()
{
    display.setup();
}

void loop()
{
    for (int x = 0; x < 16; ++x)
    {
        for (int y = 0; y < 32; ++y)
        {
            display.turnOnPixel ({ x, y });
            delay (100);
            display.turnOffPixel ({ x, y });
            delay (100);
        }
    }

    //display.turnOnPixel({ 0, 0});
}