import fileinput
from enum import Enum, auto
from typing import TypeVar
from more_itertools import locate, pairwise
from collections import Counter


class Tile(Enum):
    Empty = auto()
    Fixed = auto()
    Free = auto()


def char_to_tile(c: str) -> Tile:
    match c:
        case ".":
            return Tile.Empty
        case "#":
            return Tile.Fixed
        case "O":
            return Tile.Free
        case _:
            raise RuntimeError


Platform = list[list[Tile]]

T = TypeVar("T")


def transpose(li: list[list[T]]) -> list[list[T]]:
    return list(map(list, zip(*li)))


def reverse_rows(li: list[list[T]]) -> list[list[T]]:
    return list(map(lambda row: list(reversed(row)), li))


def rotate(li: list[list[T]]) -> list[list[T]]:
    return transpose(reverse_rows(li))


def move_rocks(li: Platform):
    for row in li:
        row_pad = [Tile.Fixed] + row + [Tile.Fixed]
        for p in pairwise(locate(row_pad, lambda t: t == Tile.Fixed)):
            if p[1] == p[0] + 1:
                continue

            c = Counter(row[p[0] : p[1] - 1])[Tile.Free]
            if c == 0:
                continue

            row[p[0] : p[1] - 1] = c * [Tile.Free] + (p[1] - p[0] - c - 1) * [
                Tile.Empty
            ]


def calculate_load(li: Platform) -> int:
    return sum(
        map(
            lambda row: sum(
                map(
                    lambda pos: len(li[0]) - pos,
                    locate(row, lambda t: t == Tile.Free),
                )
            ),
            li,
        )
    )


def as_string(li: Platform) -> str:
    return "".join(map(lambda row: "".join(map(str, row)), li))


def do_cycle(li: Platform) -> Platform:
    for _ in range(4):
        move_rocks(li)
        li = rotate(li)

    return li


def num_cycles_until_cfg_appears_twice(li: Platform) -> tuple[int, Platform]:
    seen: set[str] = set()
    num = 0
    while True:
        seen.add(as_string(li))
        li = do_cycle(li)
        num += 1

        cfg = as_string(li)
        if cfg in seen:
            break

    return (num, li)


input = transpose(
    list(
        map(
            lambda line: list(map(char_to_tile, str.rstrip(line))),
            fileinput.input(),
        )
    )
)

init, input = num_cycles_until_cfg_appears_twice(input)
cycle, input = num_cycles_until_cfg_appears_twice(input)

steps_past_cycle = (1000000000 - init) % cycle

for _ in range(steps_past_cycle):
    input = do_cycle(input)

print(calculate_load(input))
