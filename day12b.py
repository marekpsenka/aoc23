import fileinput
from functools import cache


def parse_line(line: str) -> tuple[str, tuple[int, ...]]:
    record_part, signature_part = line.split()
    return (
        "?".join([record_part] * 5) + ".",
        tuple(map(int, signature_part.split(","))) * 5,
    )


records_signatures = list(
    map(lambda ii: parse_line(str.rstrip(ii)), fileinput.input())
)


@cache
def count_arrangements(s: str, sig: tuple[int, ...]) -> int:
    if len(sig) == 0:
        if "#" in s:
            return 0
        else:
            return 1

    n = sig[0]
    count = 0
    for i in range(len(s) - sum(sig) - (len(sig) - 1)):
        if s[i + n] == "#":
            continue
        if "#" in s[:i]:
            break
        if "." not in s[i : (i + n)]:
            count += count_arrangements(s[(i + n + 1) :], sig[1:])

    return count


print(sum(map(lambda p: count_arrangements(*p), records_signatures)))
