import fileinput
from operator import itemgetter

input = map(str.rstrip, fileinput.input())

max_red = 12
max_green = 13
max_blue = 14


def is_comp_possible(comp_str: str) -> bool:
    num_str, kind_str = comp_str.split(" ")
    match kind_str:
        case "red":
            return int(num_str) <= max_red
        case "green":
            return int(num_str) <= max_green
        case "blue":
            return int(num_str) <= max_blue
        case _:
            raise RuntimeError


def is_draw_possible(draw_str: str) -> bool:
    comp_strs = draw_str.split(", ")
    return all(map(is_comp_possible, comp_strs))


def analyze_game(line: str) -> tuple[int, bool]:
    game_part, draws_part = line.split(": ")
    _, id_part = game_part.split(" ")
    draw_strs = draws_part.split("; ")
    return (int(id_part), all(map(is_draw_possible, draw_strs)))


print(sum(map(itemgetter(0), filter(itemgetter(1), map(analyze_game, input)))))
