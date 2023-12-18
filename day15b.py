import fileinput
from collections import OrderedDict
from itertools import takewhile


def _hash(s: str) -> int:
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val = val % 256

    return val


input = next(map(str.rstrip, fileinput.input()))

instructions = input.split(",")
boxes: list[OrderedDict[str, int]] = [OrderedDict() for _ in range(256)]

for ins in instructions:
    label = "".join(takewhile(str.isalpha, ins))
    h = _hash(label)
    match ins[len(label)]:
        case "-":
            if label in boxes[h]:
                boxes[h].pop(label)
        case "=":
            boxes[h][label] = int(ins[len(label) + 1])
        case _:
            raise RuntimeError

power = 0

for i, box in enumerate(boxes):
    for pos, focus in enumerate(box.values()):
        power += (i + 1) * (pos + 1) * focus

print(power)
