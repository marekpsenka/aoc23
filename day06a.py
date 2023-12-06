import fileinput
from math import sqrt, floor, ceil, prod

input = map(str.rstrip, fileinput.input())

_, times_part = next(input).split(":")
_, distances_part = next(input).split(":")

times = map(int, times_part.split())
distances = map(int, distances_part.split())


def nearest_larger_integer(x: float) -> int:
    c = ceil(x)
    if float(c) > x:
        return c
    else:
        return c + 1


def nearest_smaller_integer(x: float) -> int:
    f = floor(x)
    if float(f) < x:
        return f
    else:
        return f - 1


def possible_held_time(time: int, distance: int) -> tuple[int, int]:
    sqrt_discriminant = sqrt(time * time - 4 * distance)
    return (
        nearest_larger_integer((time - sqrt_discriminant) / 2.0),
        nearest_smaller_integer((time + sqrt_discriminant) / 2.0),
    )


def num_possibilities(time: int, distance: int) -> int:
    pt = possible_held_time(time, distance)
    return pt[1] - pt[0] + 1


print(prod(map(lambda p: num_possibilities(*p), zip(times, distances))))
