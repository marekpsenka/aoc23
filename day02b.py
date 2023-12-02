import fileinput
from functools import reduce

input = map(str.rstrip, fileinput.input())

Rgb = tuple[int, int, int]


def componentwise_max(t1: Rgb, t2: Rgb) -> Rgb:
    return (max(t1[0], t2[0]), max(t1[1], t2[1]), max(t1[2], t2[2]))


def parse_rgb(comp_str: str) -> Rgb:
    num_str, kind_str = comp_str.split(" ")
    match kind_str:
        case "red":
            return (int(num_str), 0, 0)
        case "green":
            return (0, int(num_str), 0)
        case "blue":
            return (0, 0, int(num_str))


def max_over_draw(draw_str: str) -> Rgb:
    comp_strs = draw_str.split(", ")
    return reduce(componentwise_max, map(parse_rgb, comp_strs))


def power_of_game(line: str) -> Rgb:
    game_part, draws_part = line.split(": ")
    _, id_part = game_part.split(" ")
    draw_strs = draws_part.split("; ")
    x = reduce(componentwise_max, map(max_over_draw, draw_strs))
    return x[0] * x[1] * x[2]


print(sum(map(power_of_game, input)))
