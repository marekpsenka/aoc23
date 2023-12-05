import fileinput
from more_itertools import split_before, chunked, flatten
from dataclasses import dataclass
from functools import reduce


@dataclass
class RangeMapping:
    dest_start: int
    src_start: int
    length: int

    def dest_end(self) -> int:
        return self.dest_start + self.length

    def src_end(self) -> int:
        return self.src_start + self.length

    def src_range(self) -> tuple[int, int]:
        return (self.src_start, self.src_start + self.length)

    def dest_range(self) -> tuple[int, int]:
        return (self.dest_start, self.dest_start + self.length)


SortedRangeMappings = list[RangeMapping]


def apply_mappings(
    ms: SortedRangeMappings, r: tuple[int, int]
) -> list[tuple[int, int]]:
    output: list[tuple[int, int]] = []

    if ms[0].src_start >= r[1]:
        return [r]

    i = 0
    left_pivot = r[0]
    while i < len(ms) and ms[i].src_start < r[1]:
        if r[0] > ms[i].src_end():
            i += 1
            continue

        if left_pivot < ms[i].src_start:
            output.append((left_pivot, ms[i].src_start))

        left_pivot = max(ms[i].src_start, r[0])
        right_pivot = min(r[1], ms[i].src_end())

        output.append(
            (
                ms[i].dest_start + (left_pivot - ms[i].src_start),
                ms[i].dest_start + (right_pivot - ms[i].src_start),
            ),
        )

        left_pivot = right_pivot
        i += 1

    if left_pivot < r[1]:
        output.append((left_pivot, r[1]))

    return output


def parse_range(s: str) -> RangeMapping:
    dest_start, src_start, length = map(int, s.split())
    return RangeMapping(dest_start, src_start, length)


def parse_mapping(str_list: list[str]) -> SortedRangeMappings:
    return sorted(map(parse_range, str_list[2:]), key=lambda m: m.src_start)


def apply_mappings_to_ranges(
    ranges: list[tuple[int, int]], mappings: SortedRangeMappings
) -> list[tuple[int, int]]:
    return list(flatten(map(lambda r: apply_mappings(mappings, r), ranges)))


def apply_all_mappings_to_ranges(
    ranges: list[tuple[int, int]], mappings: list[SortedRangeMappings]
) -> list[tuple[int, int]]:
    return reduce(
        lambda rs, m: apply_mappings_to_ranges(rs, m), mappings, ranges
    )


input = map(str.rstrip, fileinput.input())
input_parts = split_before(input, lambda line: not line)
_, seed_number_part = next(input_parts)[0].split(": ")
seeds = list(map(int, seed_number_part.split()))
mappings = list(map(parse_mapping, input_parts))
seed_ranges = list(map(lambda p: (p[0], p[0] + p[1]), chunked(seeds, 2)))

print(
    min(
        apply_all_mappings_to_ranges(seed_ranges, mappings), key=lambda p: p[0]
    )[0]
)
