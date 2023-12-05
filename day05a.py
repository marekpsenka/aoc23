import fileinput
from more_itertools import split_before
from dataclasses import dataclass
from functools import reduce


@dataclass
class Range:
    dest_start: int
    src_start: int
    length: int


Mapping = list[Range]


def apply_mapping(m: Mapping, arg: int) -> int:
    for r in m:
        if r.src_start <= arg and arg < r.src_start + r.length:
            return r.dest_start + (arg - r.src_start)

    return arg


def parse_range(s: str) -> Range:
    dest_start, src_start, length = map(int, s.split())
    return Range(dest_start, src_start, length)


def parse_mapping(str_list: list[str]) -> Mapping:
    return list(map(parse_range, str_list[2:]))


input = map(str.rstrip, fileinput.input())
input_parts = split_before(input, lambda line: not line)
_, seed_number_part = next(input_parts)[0].split(": ")
seeds = list(map(int, seed_number_part.split()))
mappings = list(map(parse_mapping, input_parts))


def location_number(arg: int, mappings: list[Mapping]) -> int:
    return reduce(lambda a, m: apply_mapping(m, a), mappings, arg)


print(min(map(lambda s: location_number(s, mappings), seeds)))
