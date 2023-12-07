import fileinput
from collections import Counter
from enum import Enum
from functools import cmp_to_key


class HandType(Enum):
    HighCard = 1
    OnePair = 2
    TwoPair = 3
    ThreeOfAKind = 4
    FullHouse = 5
    FourOfAKind = 6
    FiveOfAKind = 7


card_value = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def read_hand_type(hand: str) -> HandType:
    c = Counter(hand)
    match sorted(c.values()):
        case [1, 1, 1, 1, 1]:
            return HandType.HighCard
        case [1, 1, 1, 2]:
            return HandType.OnePair
        case [1, 2, 2]:
            return HandType.TwoPair
        case [1, 1, 3]:
            return HandType.ThreeOfAKind
        case [2, 3]:
            return HandType.FullHouse
        case [1, 4]:
            return HandType.FourOfAKind
        case [5]:
            return HandType.FiveOfAKind
        case _:
            raise RuntimeError


def card_based_compare(hand1: str, hand2: str) -> int:
    for c1, c2 in zip(hand1, hand2):
        if card_value[c1] > card_value[c2]:
            return 1
        elif card_value[c1] < card_value[c2]:
            return -1

    return 0


def compare_hands(hand1: str, hand2: str) -> int:
    type1 = read_hand_type(hand1)
    type2 = read_hand_type(hand2)

    if type1.value > type2.value:
        return 1
    elif type1.value < type2.value:
        return -1
    else:
        return card_based_compare(hand1, hand2)


input = map(str.rstrip, fileinput.input())


def parse_hand_bid(s: str) -> tuple[str, int]:
    hand_part, bid_part = s.split()
    return (hand_part, int(bid_part))


def compare_hands_bids(hb1: tuple[str, int], hb2: tuple[str, int]) -> int:
    return compare_hands(hb1[0], hb2[0])


hands_bids = list(map(parse_hand_bid, input))

srt = sorted(hands_bids, key=cmp_to_key(compare_hands_bids))

print(sum(map(lambda p: (p[0] + 1) * p[1][1], enumerate(srt))))
