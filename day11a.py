import fileinput
from itertools import takewhile, combinations
from more_itertools import locate, transpose

input = list(map(str.rstrip, fileinput.input()))

row_voids = list(
    locate(input, lambda line: all(map(lambda c: c == ".", line)))
)
column_voids = list(
    locate(transpose(input), lambda line: all(map(lambda c: c == ".", line)))
)

print(row_voids)
print(column_voids)


def index_after_expansion(voids: list[int], index: int) -> int:
    return index + sum(1 for _ in takewhile(lambda v: v < index, voids))


galaxies: set[tuple[int, int]] = set()

for i in range(len(input)):
    for j in range(len(input[0])):
        if input[i][j] == "#":
            galaxies.add(
                (
                    index_after_expansion(row_voids, i),
                    index_after_expansion(column_voids, j),
                )
            )


def manhattan(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


print(sum(map(lambda p: manhattan(p[0], p[1]), combinations(galaxies, 2))))
