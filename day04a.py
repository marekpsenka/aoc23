import fileinput

input = map(str.rstrip, fileinput.input())

total = 0


def parse_set(s: str) -> set[int]:
    return set(map(int, s.split()))


for line in input:
    _, numbers_part = line.split(": ")
    winning_part, mine_part = numbers_part.split(" | ")
    num_winning = len(
        parse_set(winning_part).intersection(parse_set(mine_part))
    )

    if num_winning > 0:
        total += pow(2, num_winning - 1)


print(total)
