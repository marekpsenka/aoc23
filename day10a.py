import fileinput
from enum import Enum
from typing import Optional
from more_itertools import locate


class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4


def move(p: tuple[int, int], dir: Direction) -> tuple[int, int]:
    match dir:
        case Direction.Up:
            return (p[0] - 1, p[1])
        case Direction.Down:
            return (p[0] + 1, p[1])
        case Direction.Left:
            return (p[0], p[1] - 1)
        case Direction.Right:
            return (p[0], p[1] + 1)


def flow(tile: str, dir: Direction) -> Optional[Direction]:
    match tile:
        case "-":
            match dir:
                case Direction.Right:
                    return Direction.Right
                case Direction.Left:
                    return Direction.Left
                case _:
                    return None
        case "|":
            match dir:
                case Direction.Up:
                    return Direction.Up
                case Direction.Down:
                    return Direction.Down
                case _:
                    return None
        case "F":
            match dir:
                case Direction.Left:
                    return Direction.Down
                case Direction.Up:
                    return Direction.Right
                case _:
                    return None
        case "L":
            match dir:
                case Direction.Left:
                    return Direction.Up
                case Direction.Down:
                    return Direction.Right
                case _:
                    return None
        case "J":
            match dir:
                case Direction.Right:
                    return Direction.Up
                case Direction.Down:
                    return Direction.Left
                case _:
                    return None
        case "7":
            match dir:
                case Direction.Right:
                    return Direction.Down
                case Direction.Up:
                    return Direction.Left
                case _:
                    return None
        case ".":
            return None
        case _:
            raise RuntimeError


def within_bounds(i: int, j: int, max_i: int, max_j: int) -> bool:
    if i < 0:
        return False
    elif i >= max_i:
        return False
    elif j < 0:
        return False
    elif j >= max_j:
        return False
    else:
        return True


input = list(map(str.rstrip, fileinput.input()))

start_i = next(locate(input, lambda line: "S" in line))
start_j = input[start_i].index("S")

for line in input:
    print(line)

print(start_i, start_j)

for dir in Direction:
    i, j = move((start_i, start_j), dir)
    if not within_bounds(i, j, len(input), len(input[0])):
        continue

    tile = input[i][j]
    next_dir = flow(tile, dir)
    if next_dir is None:
        continue

    length = 1
    while True:
        assert next_dir is not None
        i, j = move((i, j), next_dir)
        tile = input[i][j]
        if tile == "S":
            break
        next_dir = flow(tile, next_dir)
        length += 1

    print((length + 1) // 2)
    break
