
#pragma once

enum struct Direction
{
    left,
    right,
    up,
    down
};


// =====================================================================================
// TDD Point & Array: https://godbolt.org

struct Point
{
    int x = 0;
    int y = 0;

    bool operator== (const Point& other) const noexcept { return x == other.x && y == other.y; }
    bool operator!= (const Point& other) const noexcept { return ! (*this == other); }
};


struct WrappingPointMover
{
    WrappingPointMover (int maxX, int maxY) : maxX { maxX }, maxY { maxY } {}

    explicit WrappingPointMover (const Point& maxCoords) : maxX { maxCoords.x }, maxY { maxCoords.y } {}

    void movePoint (Point& point, Direction direction) const noexcept
    {
        if (direction == Direction::left)
            point.x -= 1;
        if (direction == Direction::right)
            point.x += 1;
        if (direction == Direction::up)
            point.y += 1;
        if (direction == Direction::down)
            point.y -= 1;

        if (point.y < 0)
            point.y = maxY;
        if (point.y > maxY)
            point.y = 0;

        if (point.x < 0)
            point.x = maxX;
        if (point.x > maxX)
            point.x = 0;
    }

    void movePointInOppositeDirection (Point& point, Direction direction) const
    {
        if (direction == Direction::left)
            return movePoint (point, Direction::right);
        if (direction == Direction::right)
            return movePoint (point, Direction::left);
        if (direction == Direction::up)
            return movePoint (point, Direction::down);

        return movePoint (point, Direction::up);
    }

    int maxX, maxY;
};


template <typename T, int MaxSize>
struct Array
{
    int getSize() { return size; }

    T& operator[] (int index)
    {
        return data[index];
    }

    void append (const T& item)
    {
        data[size++] = item;
    }

    void clear()
    {
        size = 0;
    }

    T* begin() { return data; }
    T* end() { return &data[size]; }

    const T* begin() const { return data; }
    const T* end() const { return &data[size]; }

private:
    int size = 0;
    T data[MaxSize] = {};
};

struct DisplayController;

struct Drawable
{
    virtual void draw (DisplayController& displayController) = 0;
};
