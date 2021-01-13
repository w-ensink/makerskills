
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
        if (! player.isPlaying())
            player.play (sound.data);
        else if (! player2.isPlaying())
            player2.play (sound.data);
        else if (! player3.isPlaying())
            player3.play (sound.data);
        else
            player4.play (sound.data);
    }

private:
    AudioPlayMemory player;
    AudioPlayMemory player2;
    AudioPlayMemory player3;
    AudioPlayMemory player4;
    AudioMixer4 mixer;
    AudioOutputAnalog output;
    AudioConnection c { player, mixer };
    AudioConnection c2 { player2, mixer };
    AudioConnection c3 { player3, mixer };
    AudioConnection c4 { player4, mixer };
    AudioConnection c5 { mixer, output };
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
