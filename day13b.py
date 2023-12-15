import fileinput
from more_itertools import split_at
from typing import Optional
from operator import itemgetter


def transpose(li: list[list[bool]]) -> list[list[bool]]:
    return list(map(list, zip(*li)))


def conv(c: str) -> bool:
    if c == "#":
        return True
    else:
        return False


input = map(lambda line: list(map(conv, str.rstrip(line))), fileinput.input())

patterns = list(split_at(input, lambda line: not line))


def diff(s1: list[bool], s2: list[bool]) -> list[int]:
    return list(
        map(
            itemgetter(0),
            filter(lambda p: p[1][0] != p[1][1], enumerate(zip(s1, s2))),
        )
    )


def find_axis_with_one_smudge(rs: list[list[bool]]) -> Optional[int]:
    for i in range(len(rs) - 1):
        diffs: list[tuple[int, int]] = []
        for j in range(min(i + 1, len(rs) - i - 1)):
            diffs += map(lambda k: (i - j, k), diff(rs[i - j], rs[i + j + 1]))

        if len(diffs) == 1:
            return i

    return None


sum_of_column_numbers_to_the_left = 0
sum_of_row_counts_above = 0

for pattern in patterns:
    axis = find_axis_with_one_smudge(pattern)
    if axis is not None:
        sum_of_row_counts_above += axis + 1
    else:
        axis = find_axis_with_one_smudge(list(transpose(pattern)))
        if axis is not None:
            sum_of_column_numbers_to_the_left += axis + 1

print(sum_of_column_numbers_to_the_left + 100 * sum_of_row_counts_above)
