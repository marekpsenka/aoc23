import fileinput

input = list(map(str.rstrip, fileinput.input()))
num_cards = [1 for _ in input]


def parse_set(s: str) -> set[int]:
    return set(map(int, s.split()))


for i, line in enumerate(input):
    _, numbers_part = line.split(": ")
    winning_part, mine_part = numbers_part.split(" | ")
    num_winning = len(
        parse_set(winning_part).intersection(parse_set(mine_part))
    )
    for j in range(i + 1, min(len(input), i + 1 + num_winning)):
        num_cards[j] += num_cards[i]

print(sum(num_cards))
