import math


def fuel(m):
    return max(math.floor(m / 3) - 2, 0)


assert fuel(12) == 2
assert fuel(14) == 2
assert fuel(1969) == 654
assert fuel(100756) == 33583

modules = []
with open("d01_input.txt") as f:
    for line in f:
        modules.append(int(line.strip()))

print("Part1 =", sum(map(fuel, modules)))


def recursive_fuel(m):
    fm = fuel(m)
    return fm + recursive_fuel(fm) if fm > 0 else 0


assert recursive_fuel(12) == 2
assert recursive_fuel(1969) == 966
assert recursive_fuel(100756) == 50346

print("Part2 =", sum(map(recursive_fuel, modules)))
