import fileinput


def _hash(s: str) -> int:
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val = val % 256

    return val


input = next(map(str.rstrip, fileinput.input()))

print(sum(map(_hash, input.split(","))))
