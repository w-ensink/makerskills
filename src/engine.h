
#pragma once

#include "display.h"
#include "joy_stick.h"
#include "sounds.h"
// =============================================================================================

struct AudioController
{
    void setup()
    {
        AudioMemory (32);

    }

    void playSound (const Sound& sound)
    {
        player.play (sound.data);
    }

private:


   // Array<AudioPlayMemory, 4> soundPlayers;
   // Array<AssignableAudioConnection, 5> connections;
    AudioPlayMemory player;
    AudioMixer4 mixer;
    AudioOutputAnalog output;
    AudioConnection c { player, output };
};

// =============================================================================================


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

    AudioController& getAudioController() noexcept { return audioController; }

    void setup()
    {
        leftJoyStick.setup();
        rightJoyStick.setup();
        displayController.setup();
        audioController.setup();
    }

    void update()
    {
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

    AudioController audioController;
};
