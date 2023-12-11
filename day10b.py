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

max_i = len(input)
max_j = len(input[0])

print(start_i, start_j)

loop_points: set[tuple[int, int]] = set()
dirs_at_loop_points: dict[tuple[int, int], Direction] = dict()

for dir in Direction:
    i, j = move((start_i, start_j), dir)
    if not within_bounds(i, j, max_i, max_j):
        continue

    tile = input[i][j]
    next_dir = flow(tile, dir)
    if next_dir is None:
        continue
    loop_points.add((start_i, start_j))
    dirs_at_loop_points[(start_i, start_j)] = dir

    while True:
        assert next_dir is not None
        loop_points.add((i, j))
        dirs_at_loop_points[(i, j)] = next_dir

        i, j = move((i, j), next_dir)
        tile = input[i][j]
        if tile == "S":
            break
        next_dir = flow(tile, next_dir)

    break

left_points: set[tuple[int, int]] = set()
right_points: set[tuple[int, int]] = set()

inside_tiles = 0

for i in range(max_i):
    inside = False
    for j in range(max_j):
        if (i, j) in loop_points:
            match input[i][j]:
                case "|" | "L" | "J":
                    inside = not inside
                case _:
                    pass
        elif inside:
            inside_tiles += 1

print(inside_tiles)
