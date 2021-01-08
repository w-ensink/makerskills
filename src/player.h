
#pragma once

#include "food.h"
#include "joy_stick.h"
#include "utility.h"


struct Player : public Drawable
{
    explicit Player (Engine& e) : pointMover { e.getDisplayController().getResolution() }
    {
    }

    void changeDirection (Direction newDirection)
    {
        currentDirection = newDirection;
    }

    void draw (DisplayController& displayController) override
    {
        displayController.turnOnPixel (head);

        for (auto& p : tail)
            displayController.turnOnPixel (p);
    }

    // checks if this player has run into the other player (so it loses)
    bool ranIntoOther (const Player& other) const
    {
        if (head == other.head)
            return true;

        for (auto& p : other.tail)
            if (head == p)
                return true;

        return false;
    }

    bool ranIntoItself() const
    {
        for (auto& p : tail)
            if (p == head)
                return true;

        return false;
    }

    bool canGrabFood (const Food& food) const
    {
        return head == food.position;
    }

    void increaseTail()
    {
        if (tail.getSize() > 0)
        {
            auto p = *(tail.end() - 1);
            pointMover.movePointInOppositeDirection (p, currentDirection);
            tail.append (p);
        }
        else
        {
            auto p = head;
            pointMover.movePointInOppositeDirection (p, currentDirection);
            tail.append (p);
        }
    }

    void removeTail()
    {
        tail.clear();
    }

    void update()
    {
        if (tail.getSize() > 0)
        {
            decltype (tail) newTail {};
            newTail.append (head);

            for (auto i = 0; i < tail.getSize() - 1; ++i)
                newTail.append (tail[i]);

            tail.clear();

            for (auto p : newTail)
                tail.append (p);
        }

        pointMover.movePoint (head, currentDirection);
    }

private:
    Direction currentDirection = Direction::up;
    WrappingPointMover pointMover;
    Point head;
    Array<Point, 128> tail;
};