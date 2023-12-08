import fileinput
from itertools import cycle

input = map(str.rstrip, fileinput.input())

instructions = next(input)
_ = next(input)


def parse_node(line: str) -> tuple[str, tuple[str, str]]:
    here, dests_part = line.split(" = ")
    left, right = dests_part[1 : (len(dests_part) - 1)].split(", ")
    return (here, (left, right))


network = dict(map(parse_node, input))

length = 0
current_node = "AAA"
instruction_cycle = cycle(instructions)

while current_node != "ZZZ":
    match next(instruction_cycle):
        case "L":
            current_node = network[current_node][0]
        case "R":
            current_node = network[current_node][1]
        case _:
            raise RuntimeError

    length += 1

print(length)
