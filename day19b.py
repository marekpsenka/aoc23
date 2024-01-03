import fileinput
from more_itertools import split_at, locate
from dataclasses import dataclass
from copy import copy
from typing import Optional
from math import prod


@dataclass
class Conditional:
    category: str
    operator: str
    value: int
    goto: str


Rule = Conditional | str
Range = tuple[int, int]
Ranges = dict[str, Range]


def parse_rule(s: str) -> Rule:
    if ":" in s:
        cond_part, goto = s.split(":")
        op_idx = next(locate(cond_part, lambda c: not c.isalnum()))
        return Conditional(
            cond_part[:op_idx],
            cond_part[op_idx],
            int(cond_part[(op_idx) + 1 :]),
            goto,
        )
    else:
        return s


def parse_workflow(s: str) -> tuple[str, list[Rule]]:
    id, rules_part = s.split("{")
    rules = list(map(parse_rule, rules_part[:-1].split(",")))
    return (id, rules)


def low_pass(r: Range, v: int) -> tuple[Optional[Range], Optional[Range]]:
    rmin, rmax = r
    if rmin >= v:
        return (None, (rmin, rmax))
    elif v <= rmax:
        return ((rmin, v - 1), (v, rmax))
    else:
        return ((rmin, rmax), None)


def high_pass(r: Range, v: int) -> tuple[Optional[Range], Optional[Range]]:
    rmin, rmax = r
    if rmax <= v:
        return (None, (rmin, rmax))
    elif v >= rmin:
        return ((v + 1, rmax), (rmin, v))
    else:
        return ((rmin, rmax), None)


def derive(
    rs: Ranges, category: str, new_range: Optional[Range]
) -> Optional[Ranges]:
    if new_range is None:
        return None
    else:
        new_rs = copy(rs)
        new_rs[category] = new_range
        return new_rs


def filter(
    rs: Ranges, c: Conditional
) -> tuple[Optional[Ranges], Optional[Ranges]]:
    match c.operator:
        case "<":
            consumed, kept = low_pass(rs[c.category], c.value)
        case ">":
            consumed, kept = high_pass(rs[c.category], c.value)
        case _:
            raise RuntimeError

    return (derive(rs, c.category, consumed), derive(rs, c.category, kept))


accepted: list[Ranges] = list()


def propagate(rs: Ranges, wf: str):
    match wf:
        case "R":
            return
        case "A":
            accepted.append(rs)
            return
        case _:
            for rule in wfs[wf]:
                match rule:
                    case Conditional(_):
                        consumed, kept = filter(rs, rule)
                        if consumed is not None:
                            propagate(consumed, rule.goto)
                        if kept is None:
                            break
                        else:
                            rs = kept
                    case str(_):
                        return propagate(rs, rule)

            raise RuntimeError


def cardinality(rs: Ranges) -> int:
    return prod(map(lambda r: r[1] - r[0] + 1, rs.values()))


input = split_at(map(str.rstrip, fileinput.input()), lambda line: not line)
wfs = dict(map(parse_workflow, next(input)))

propagate(
    {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}, "in"
)

print(sum(map(cardinality, accepted)))
