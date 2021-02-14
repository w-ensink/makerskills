
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

        if (currentContext != nullptr)
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
    struct ScoreBoard
    {
        enum struct Winner
        {
            none,
            left,
            right
        };

        Winner winner = Winner::none;
    };

    struct InGameContext : Context, JoyStick::Listener
    {
        explicit InGameContext (Snake& s) : snake { s }, leftPlayer { s.engine }, rightPlayer { s.engine } {}

        void joyStickUpdate (JoyStick& joyStick, Direction direction) override
        {
            if (&snake.engine.getLeftJoyStick() == &joyStick)
                leftPlayer.changeDirection (direction);

            if (&snake.engine.getRightJoyStick() == &joyStick)
                rightPlayer.changeDirection (direction);

            snake.engine.getAudioController().playSound (sounds::turnSound);
        }

        void onContextEnter() override
        {
            snake.engine.getLeftJoyStick().setListener (this);
            snake.engine.getRightJoyStick().setListener (this);

            leftPlayer.removeTail();
            rightPlayer.removeTail();

            generateNewFoodPosition();
            givePlayersRandomPositions();

            snake.engine.getAudioController().playSound (sounds::startGame);
        }

        void onContextExit() override
        {
        }

        void update() override
        {
            leftPlayer.update();
            rightPlayer.update();

            auto leftRanIntoRight = leftPlayer.ranIntoOther (rightPlayer);
            auto rightRanIntoLeft = rightPlayer.ranIntoOther (leftPlayer);

            if (leftRanIntoRight && rightRanIntoLeft)
            {
                auto leftTailLength = leftPlayer.getTailLength();
                auto rightTailLength = rightPlayer.getTailLength();

                if (leftTailLength == rightTailLength)
                    return gameOverTie();

                if (leftTailLength > rightTailLength)
                    return gameOverLeftWon();

                return gameOverRightWon();
            }

            if (leftRanIntoRight || leftPlayer.ranIntoItself())
                return gameOverRightWon();

            if (rightRanIntoLeft || rightPlayer.ranIntoItself())
                return gameOverLeftWon();

            if (leftPlayer.canGrabFood (food))
            {
                leftPlayer.increaseTail();
                generateNewFoodPosition();
                snake.engine.getAudioController().playSound (sounds::leftFood);
            }

            if (rightPlayer.canGrabFood (food))
            {
                rightPlayer.increaseTail();
                generateNewFoodPosition();
                snake.engine.getAudioController().playSound (sounds::rightFood);
            }
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

        void gameOverLeftWon()
        {
            snake.scoreBoard.winner = ScoreBoard::Winner::left;
            snake.engine.getAudioController().playSound (sounds::rightCrash);
            snake.switchContextTo (&snake.menuContext);
        }

        void gameOverRightWon()
        {
            snake.scoreBoard.winner = ScoreBoard::Winner::right;
            snake.engine.getAudioController().playSound (sounds::leftCrash);
            snake.switchContextTo (&snake.menuContext);
        }

        void gameOverTie()
        {
            snake.scoreBoard.winner = ScoreBoard::Winner::none;
            snake.engine.getAudioController().playSound (sounds::draw);
            snake.switchContextTo (&snake.menuContext);
        }

        void givePlayersRandomPositions()
        {
            auto firstPoint = Point { random() % 16, random() % 32 };
            auto secondPoint = Point { random() % 16, random() % 32 };

            while (firstPoint == secondPoint)
                secondPoint = Point { random() % 16, random() % 32 };

            leftPlayer.setPosition (firstPoint);
            rightPlayer.setPosition (secondPoint);
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
            {
                if (snake.scoreBoard.winner == ScoreBoard::Winner::left)
                    dc.drawImage (images::arrowLeft);
                if (snake.scoreBoard.winner == ScoreBoard::Winner::right)
                    dc.drawImage (images::arrowRight);
                if (snake.scoreBoard.winner == ScoreBoard::Winner::none)
                    dc.drawImage (images::doubleArrow);
            }
        }

        Snake& snake;
        int frame = 0;
    };


    // ===============================================================================

    void setup() override
    {
        switchContextTo (&menuContext);
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
    ScoreBoard scoreBoard;
};