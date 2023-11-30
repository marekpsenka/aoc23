import fileinput

input = map(str.rstrip, fileinput.input())

for line in input:
    print(line)
