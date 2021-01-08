#include <Arduino.h>
#include "engine.h"
#include "snake.h"

auto engine = Engine {};
auto snake = Snake { engine };

void setup()
{
    engine.setup();
    snake.setup();
    Serial.begin(9600);
}

void loop()
{
    engine.update();
    snake.update();
    snake.draw();
    delay (150);

}