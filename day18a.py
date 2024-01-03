import fileinput
from enum import Enum, auto


class Direction(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()

    def opposite(self) -> "Direction":
        match self:
            case Direction.Up:
                return Direction.Down
            case Direction.Down:
                return Direction.Up
            case Direction.Right:
                return Direction.Left
            case Direction.Left:
                return Direction.Right


Point = tuple[int, int]


def move(p: Point, dir: Direction, dist: int) -> Point:
    match dir:
        case Direction.Up:
            return (p[0] - dist, p[1])
        case Direction.Down:
            return (p[0] + dist, p[1])
        case Direction.Left:
            return (p[0], p[1] - dist)
        case Direction.Right:
            return (p[0], p[1] + dist)


def manhattan(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


input = map(str.rstrip, fileinput.input())

area = 0
boundary = 0

p = (0, 0)
new_p = (0, 0)
for line in input:
    dir, count_str, color = line.split()
    count = int(count_str)
    match dir:
        case "R":
            new_p = move(p, Direction.Right, count)
        case "L":
            new_p = move(p, Direction.Left, count)
        case "D":
            new_p = move(p, Direction.Down, count)
        case "U":
            new_p = move(p, Direction.Up, count)
        case _:
            raise RuntimeError

    area += p[0] * new_p[1] - p[1] * new_p[0]
    boundary += count
    p = new_p

print((-area + boundary) / 2 + 1)
