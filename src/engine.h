
#pragma once

#include "display.h"
#include "joy_stick.h"

struct Engine
{
    struct Game
    {
        explicit Game (Engine& e) : engine { e } {}
        virtual ~Game() = default;

        virtual void setup() = 0;
        virtual void update() = 0;

    protected:
        Engine& engine;
    };

    DisplayController& getDisplayController() noexcept { return displayController; }

    JoyStick& getLeftJoyStick() noexcept { return leftJoyStick; }

    JoyStick& getRightJoyStick() noexcept { return rightJoyStick; }

    void setup()
    {
        leftJoyStick.setup();
        rightJoyStick.setup();
        displayController.setup();
    }

    void update()
    {
        displayController.clearDisplay();
        leftJoyStick.update();
        rightJoyStick.update();
    }


private:
    const DisplayController::Spec displaySpec = {
        .dataInPin = 12,
        .clkPin = 11,
        .loadPin = 10,
        .numDisplays = 8
    };

    DisplayController displayController { displaySpec };

    const JoyStick::PinLayout joyStickLeftLayout = {
        .analogXPin = A6,
        .analogYPin = A5,
        .buttonClickPin = 4
    };

    const JoyStick::PinLayout joyStickRightLayout = {
        .analogXPin = A1,
        .analogYPin = A0,
        .buttonClickPin = 2
    };

    JoyStick leftJoyStick { joyStickLeftLayout };
    JoyStick rightJoyStick { joyStickRightLayout };
};
