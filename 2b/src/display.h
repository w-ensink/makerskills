
#pragma once

#include <LedControl.h>

#include "utility.h"

struct DisplayController
{
    struct Spec
    {
        int dataInPin;
        int clkPin;
        int loadPin;
        int numDisplays;
        int xResolution = 16;
        int yResolution = 32;
    };

    explicit DisplayController (const Spec& spec) : spec (spec) {}

    void setup()
    {
        for (int display = 0; display < spec.numDisplays; display++)
        {
            ledController.shutdown (display, false);
            ledController.setIntensity (display, 8);
            ledController.clearDisplay (display);
        }
    }

    void turnOnPixel (const Point& pixel) noexcept
    {
        setStateOfPixel (pixel, true);
    }

    void turnOffPixel (const Point& pixel) noexcept
    {
        setStateOfPixel (pixel, false);
    }

    Point getResolution() noexcept
    {
        return { spec.xResolution, spec.yResolution };
    }

    void clearDisplay()
    {
        for (auto d = 0; d < spec.numDisplays; ++d)
            ledController.clearDisplay (d);
    }

    void drawImage (const Image& image)
    {
        for (auto x = 0; x < 16; ++x)
        {
            auto column = image.pixels[x];
            auto mask = (uint32_t) 0x01;

            for (auto y = 0; y < 32; ++y)
            {
                auto value = (bool) (column & mask);
                mask <<= 1;
                setStateOfPixel ({ x, y }, value);
            }
        }
    }

private:
    Spec spec;

    LedControl ledController {
        spec.dataInPin,
        spec.clkPin,
        spec.loadPin,
        spec.numDisplays
    };

    void setStateOfPixel (Point pixel, bool state)
    {
        pixel.x = 15 - pixel.x;
        pixel.y = 31 - pixel.y;

        auto x = 7 - (pixel.x % 8);
        auto y = 7 - (pixel.y % 8);
        auto display = (pixel.y / 8) + (pixel.x / 8) * 4;
        ledController.setLed (display, x, y, state);
    }
};
