import fileinput
from more_itertools import split_at, transpose
from typing import Optional

input = map(lambda line: tuple(str.rstrip(line)), fileinput.input())

patterns = split_at(input, lambda line: not line)

sum_of_column_numbers_to_the_left = 0
sum_of_row_counts_above = 0


def find_axis(rs: list[tuple[str, ...]]) -> Optional[int]:
    for i in range(len(rs) - 1):
        if all(
            map(
                lambda p: p[0] == p[1],
                zip(reversed(rs[: (i + 1)]), rs[(i + 1) :]),
            )
        ):
            return i
    return None


for pattern in patterns:
    axis = find_axis(pattern)
    if axis is not None:
        sum_of_row_counts_above += axis + 1
    else:
        axis = find_axis(list(transpose(pattern)))
        if axis is not None:
            sum_of_column_numbers_to_the_left += axis + 1
        else:
            raise RuntimeError

print(sum_of_column_numbers_to_the_left + 100 * sum_of_row_counts_above)
