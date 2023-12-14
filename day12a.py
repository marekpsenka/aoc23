import fileinput
from more_itertools import run_length
from operator import itemgetter
from copy import copy


def parse_line(line: str) -> tuple[str, list[int]]:
    record_part, signature_part = line.split()
    return (record_part, list(map(int, signature_part.split(","))))


records_signatures = list(
    map(lambda ii: parse_line(str.rstrip(ii)), fileinput.input())
)


def consistent(list1: list[int], list2: list[int]) -> bool:
    if len(list1) > len(list2):
        return False
    else:
        return all(map(lambda p: p[0] <= p[1], zip(list1, list2)))


def signature(s: str) -> list[int]:
    return list(
        map(itemgetter(1), filter(lambda p: p[0] == "#", run_length.encode(s)))
    )


def str_replace_at(s: str, i: int, c: str) -> str:
    chars = list(s)
    chars[i] = c
    return "".join(chars)


#          ???.### 1,1,3
def replace_next(s: str, target_signature: list[int]) -> int:
    pos = s.find("?")
    if pos < 0:
        sig = signature(s)
        if sig == target_signature:
            return 1
        else:
            return 0
    else:
        sig = signature(s[:pos])
        if consistent(sig, target_signature):
            return replace_next(
                str_replace_at(copy(s), pos, "."), target_signature
            ) + replace_next(
                str_replace_at(copy(s), pos, "#"), target_signature
            )
        else:
            return 0


print(replace_next(*records_signatures[2]))

print(sum(map(lambda p: replace_next(*p), records_signatures)))
