import fileinput
from itertools import pairwise


def differences(seq: list[int]) -> list[int]:
    return list(map(lambda p: p[1] - p[0], pairwise(seq)))


def extrapolate(seq: list[int]) -> int:
    if all(map(lambda n: n == 0, seq)):
        return 0
    else:
        return seq[0] - extrapolate(differences(seq))


def line_to_seq(line: str) -> list[int]:
    return list(map(int, line.split()))


input = map(str.rstrip, fileinput.input())

print(sum(map(extrapolate, map(line_to_seq, input))))
