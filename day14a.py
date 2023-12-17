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


T = TypeVar("T")


def pretty_print(li: list[list[T]]):
    for r in li:
        print(r)


def transpose(li: list[list[T]]) -> list[list[T]]:
    return list(map(list, zip(*li)))


def calculate_load(row: list[Tile]) -> int:
    row = [Tile.Fixed] + row + [Tile.Fixed]
    load = 0
    for p in pairwise(locate(row, lambda t: t == Tile.Fixed)):
        c = Counter(row[p[0] : p[1]])
        load += sum(
            range(len(row) - p[0] - c[Tile.Free] - 1, len(row) - p[0] - 1)
        )
    return load


input = transpose(
    list(
        map(
            lambda line: list(map(char_to_tile, str.rstrip(line))),
            fileinput.input(),
        )
    )
)

print(sum(map(calculate_load, input)))
