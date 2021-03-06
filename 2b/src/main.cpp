#include "engine.h"
#include "snake.h"
#include <Arduino.h>

auto engine = Engine {};
auto snake = Snake { engine };

void setup()
{
    engine.setup();
    snake.setup();
}

void loop()
{
    for (auto i = 0; i < 11; ++i)
    {
        delay (10);
        engine.update();
    }

    engine.getDisplayController().clearDisplay();
    snake.update();
    snake.draw();
}