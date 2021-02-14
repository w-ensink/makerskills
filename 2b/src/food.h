
#pragma once

#include "display.h"
#include "utility.h"

struct Food : Drawable
{
    void draw (DisplayController& displayController) override
    {
        displayController.turnOnPixel (position);
    }

    Point position;
};