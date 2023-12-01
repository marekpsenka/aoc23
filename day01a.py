import fileinput

input = map(str.rstrip, fileinput.input())


def calibration_value(s: str) -> int:
    digits = list(filter(lambda c: c.isdigit(), s))
    if len(digits) >= 2:
        return int(digits[0] + digits[-1])
    elif len(digits) == 1:
        return int(digits[0] + digits[0])
    else:
        raise RuntimeError


print(sum(map(calibration_value, input)))
