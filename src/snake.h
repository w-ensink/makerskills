
#pragma once

#include "engine.h"
#include "images.h"
#include "player.h"

struct ContextSwitcher;

struct Context : Drawable
{
    ContextSwitcher& getContextSwitcher() { return *contextSwitcher; }

    virtual void onContextExit() {}
    virtual void onContextEnter() {}

    virtual void update() {}

private:
    friend struct ContextSwitcher;
    ContextSwitcher* contextSwitcher = nullptr;
};

// ===================================================================================

struct ContextSwitcher
{
    void switchContextTo (Context* to)
    {
        if (to == nullptr)
            return;

        if (currentContext)
        {
            currentContext->onContextExit();
            currentContext->contextSwitcher = nullptr;
        }
        currentContext = to;

        currentContext->contextSwitcher = this;
        currentContext->onContextEnter();
    }

    Context& getCurrentContext() { return *currentContext; }

private:
    Context* currentContext = nullptr;
};

// ===================================================================================


struct Snake : public Engine::Game, ContextSwitcher
{
    explicit Snake (Engine& e) : Engine::Game { e }, inGameContext { *this } {}

    // ===============================================================================


    struct InGameContext : Context, JoyStick::Listener
    {
        explicit InGameContext (Snake& s) : snake { s }, leftPlayer { s.engine }, rightPlayer { s.engine } {}

        void joyStickUpdate (JoyStick& joyStick, Direction direction) override
        {
            if (&snake.engine.getLeftJoyStick() == &joyStick)
                leftPlayer.changeDirection (direction);

            if (&snake.engine.getRightJoyStick() == &joyStick)
                rightPlayer.changeDirection (direction);
        }

        void onContextEnter() override
        {
            snake.engine.getLeftJoyStick().setListener (this);
            snake.engine.getRightJoyStick().setListener (this);

            leftPlayer.removeTail();
            rightPlayer.removeTail();

            generateNewFoodPosition();
        }

        void update() override
        {
            leftPlayer.update();
            rightPlayer.update();

            //auto leftRanIntoRight = leftPlayer.ranIntoOther (rightPlayer);
            // auto rightRanIntoLeft = rightPlayer.ranIntoOther (leftPlayer);

            if (leftPlayer.ranIntoItself())
                snake.switchContextTo (&snake.menuContext);

            if (rightPlayer.ranIntoItself())
                snake.switchContextTo (&snake.menuContext);

            if (leftPlayer.canGrabFood (food))
            {
                leftPlayer.increaseTail();
                generateNewFoodPosition();
            }
            if (rightPlayer.canGrabFood (food))
            {
                rightPlayer.increaseTail();
                generateNewFoodPosition();
            }

            //snake.switchContextTo (&snake.menuContext);
        }

        void draw (DisplayController& dc) override
        {
            food.draw (dc);
            leftPlayer.draw (dc);
            rightPlayer.draw (dc);
        }

    private:
        Snake& snake;
        Player leftPlayer;
        Player rightPlayer;
        Food food;

        void generateNewFoodPosition()
        {
            food.position.x = random() % 16;
            food.position.y = random() % 32;
        }
    };

    // ===============================================================================


    struct MenuContext : Context, JoyStick::Listener
    {
        explicit MenuContext (Snake& s) : snake { s } {}

        void onContextEnter() override
        {
            snake.engine.getRightJoyStick().setListener (this);
            snake.engine.getLeftJoyStick().setListener (this);
        }

        void joyStickUpdate (JoyStick&, Direction) override {}

        void joyStickButtonDown (JoyStick&) override
        {
            snake.switchContextTo (&snake.inGameContext);
        }

        void update() override
        {
            ++frame;
        }

        void draw (DisplayController& dc) override
        {
            if (frame % 2 == 0)
                dc.drawImage (images::arrowLeft);
        }

        Snake& snake;
        int frame = 0;
    };


    // ===============================================================================

    void setup() override
    {
        switchContextTo (&inGameContext);
    }

    void update() override
    {
        getCurrentContext().update();
    }

    void draw()
    {
        getCurrentContext().draw (engine.getDisplayController());
    }

private:
    InGameContext inGameContext { *this };
    MenuContext menuContext { *this };
};