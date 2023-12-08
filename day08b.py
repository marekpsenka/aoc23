import fileinput
from itertools import cycle
from math import lcm

input = map(str.rstrip, fileinput.input())

instructions = next(input)
_ = next(input)


def parse_node(line: str) -> tuple[str, tuple[str, str]]:
    here, dests_part = line.split(" = ")
    left, right = dests_part[1 : (len(dests_part) - 1)].split(", ")
    return (here, (left, right))


network = dict(map(parse_node, input))


current_nodes = list(filter(lambda s: s[-1] == "A", network.keys()))


def traverse(current: str) -> int:
    length = 0
    instruction_cycle = cycle(instructions)

    while current[-1] != "Z":
        match next(instruction_cycle):
            case "L":
                current = network[current][0]
            case "R":
                current = network[current][1]
            case _:
                raise RuntimeError

        length += 1

    return length


ls = map(traverse, current_nodes)
print(lcm(*ls))
