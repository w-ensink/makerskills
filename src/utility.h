
#pragma once

enum struct Direction
{
    left,
    right,
    up,
    down
};

Direction oppositeDirection (Direction direction)
{
    if (direction == Direction::left)
        return Direction::right;
    if (direction == Direction::right)
        return Direction::left;
    if (direction == Direction::up)
        return Direction::down;

    return Direction::up;
}

bool isVerticalDirection (Direction d)
{
    return d == Direction::up || d == Direction::down;
}

bool isHorizontalDirection (Direction d)
{
    return d == Direction::left || d == Direction::right;
}

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

    explicit WrappingPointMover (const Point& resolution) : maxX { resolution.x - 1 }, maxY { resolution.y - 1 } {}

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
        movePoint (point, oppositeDirection (direction));
    }

    int maxX, maxY;
};


template <typename T, int MaxSize>
struct Array
{
    int getSize() const { return size; }

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


// image of 16x32 pixels
struct Image
{
    uint32_t pixels[16];
};
