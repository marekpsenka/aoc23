import fileinput

input = map(str.rstrip, fileinput.input())

digit_names = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]
corresponding_digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def get_digits(s: str) -> list[str]:
    digits = []
    for i in range(len(s)):
        if s[i].isdigit():
            digits.append(s[i])
        else:
            for index, name in enumerate(digit_names):
                if s[i:].startswith(name):
                    digits.append(corresponding_digits[index])
                    break
    return digits


def calibration_value(s: str) -> int:
    digits = get_digits(s)
    if len(digits) >= 2:
        return int(digits[0] + digits[-1])
    elif len(digits) == 1:
        return int(digits[0] + digits[0])
    else:
        raise RuntimeError


print(sum(map(calibration_value, input)))
