import fileinput
from more_itertools import split_at, locate
from dataclasses import dataclass, asdict
from re import finditer


@dataclass
class Params:
    x: int
    m: int
    a: int
    s: int


@dataclass
class Conditional:
    category: str
    operator: str
    value: int
    goto: str


Rule = Conditional | str


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


def parse_params(line: str) -> Params:
    x, m, a, s = map(lambda m: int(m[0]), finditer(r"\d+", line))
    return Params(x, m, a, s)


def check_condition(ps: Params, c: Conditional) -> bool:
    match c.operator:
        case "<":
            return asdict(ps)[c.category] < c.value
        case ">":
            return asdict(ps)[c.category] > c.value
        case _:
            raise RuntimeError


def is_accepted(ps: Params, wf: str) -> bool:
    match wf:
        case "R":
            return False
        case "A":
            return True
        case _:
            for rule in wfs[wf]:
                match rule:
                    case Conditional(_):
                        if check_condition(ps, rule):
                            return is_accepted(ps, rule.goto)
                    case str(_):
                        return is_accepted(ps, rule)

            raise RuntimeError


input = split_at(map(str.rstrip, fileinput.input()), lambda line: not line)

wfs = dict(map(parse_workflow, next(input)))
parts = list(map(parse_params, next(input)))

accepted_parts = filter(lambda p: is_accepted(p, "in"), parts)
print(sum(map(lambda p: p.x + p.m + p.a + p.s, accepted_parts)))
