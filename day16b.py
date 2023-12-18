import fileinput
from enum import Enum, auto
from more_itertools import ilen
from itertools import chain


class Direction(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()


Point = tuple[int, int]


def move(p: Point, dir: Direction) -> Point:
    match dir:
        case Direction.Up:
            return (p[0] - 1, p[1])
        case Direction.Down:
            return (p[0] + 1, p[1])
        case Direction.Left:
            return (p[0], p[1] - 1)
        case Direction.Right:
            return (p[0], p[1] + 1)


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
max_i = len(input)
max_j = len(input[0])


def trace_ray_step_simple(
    p: Point, dir: Direction, tile: str
) -> tuple[Point, Direction]:
    match tile:
        case ".":
            return (move(p, dir), dir)
        case "\\":
            match dir:
                case Direction.Left:
                    return (move(p, Direction.Up), Direction.Up)
                case Direction.Right:
                    return (move(p, Direction.Down), Direction.Down)
                case Direction.Down:
                    return (move(p, Direction.Right), Direction.Right)
                case Direction.Up:
                    return (move(p, Direction.Left), Direction.Left)
        case "/":
            match dir:
                case Direction.Left:
                    return (move(p, Direction.Down), Direction.Down)
                case Direction.Right:
                    return (move(p, Direction.Up), Direction.Up)
                case Direction.Down:
                    return (move(p, Direction.Left), Direction.Left)
                case Direction.Up:
                    return (move(p, Direction.Right), Direction.Right)
        case _:
            raise RuntimeError


def trace_ray(
    origin: Point,
    init_dir: Direction,
    energized: list[list[bool]],
    ray_cache: set[tuple[Point, Direction]],
):
    p = origin
    dir = init_dir
    while True:
        if (not within_bounds(p[0], p[1], max_i, max_j)) or (
            (p, dir) in ray_cache
        ):
            break
        ray_cache.add((p, dir))
        energized[p[0]][p[1]] = True
        tile = input[p[0]][p[1]]
        match tile:
            case "." | "\\" | "/":
                p, dir = trace_ray_step_simple(p, dir, tile)

            case "|":
                if dir == Direction.Up or dir == Direction.Down:
                    p = move(p, dir)
                else:
                    p1 = move(p, Direction.Up)
                    p2 = move(p, Direction.Down)
                    if within_bounds(p1[0], p1[1], max_i, max_j):
                        trace_ray(p1, Direction.Up, energized, ray_cache)
                    if within_bounds(p2[0], p2[1], max_i, max_j):
                        trace_ray(p2, Direction.Down, energized, ray_cache)
                    break

            case "-":
                if dir == Direction.Right or dir == Direction.Left:
                    p = move(p, dir)
                else:
                    p1 = move(p, Direction.Right)
                    p2 = move(p, Direction.Left)
                    if within_bounds(p1[0], p1[1], max_i, max_j):
                        trace_ray(p1, Direction.Right, energized, ray_cache)
                    if within_bounds(p2[0], p2[1], max_i, max_j):
                        trace_ray(p2, Direction.Left, energized, ray_cache)
                    break


def count_energized(origin: Point, init_dir: Direction) -> int:
    energized = [[False for _ in range(max_j)] for _ in range(max_i)]
    ray_cache: set[tuple[Point, Direction]] = set()
    trace_ray(origin, init_dir, energized, ray_cache)
    return sum(map(lambda row: ilen(filter(None, row)), energized))


print(
    max(
        map(
            lambda p: count_energized(*p),
            chain.from_iterable(
                [
                    [((0, j), Direction.Down) for j in range(max_j)],
                    [((max_i - 1, j), Direction.Up) for j in range(max_j)],
                    [((i, 0), Direction.Right) for i in range(max_i)],
                    [((i, max_j - 1), Direction.Left) for i in range(max_i)],
                ]
            ),
        )
    )
)
