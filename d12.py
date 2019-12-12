import re
import numpy as np


s = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""

s_ = """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""

# my puzzle input
s = """
<x=-13, y=-13, z=-13>
<x=5, y=-8, z=3>
<x=-6, y=-10, z=-3>
<x=0, y=5, z=-5>
"""

moons = []
for line in s.strip().split("\n"):
    pos = list(map(int, re.findall("=([^,>]*)", line)))
    vel = [0, 0, 0]
    moons.append([pos, vel])

N = len(moons)

K = 1000
for _ in range(K):
    for m1 in range(N):
        for m2 in range(m1 + 1, N):
            for i in range(3):
                if moons[m1][0][i] < moons[m2][0][i]:
                    moons[m1][1][i] += 1
                    moons[m2][1][i] -= 1
                elif moons[m1][0][i] > moons[m2][0][i]:
                    moons[m1][1][i] -= 1
                    moons[m2][1][i] += 1

    for m in range(N):
        for i in range(3):
            moons[m][0][i] += moons[m][1][i]

    e = 0
    for m in moons:
        p = sum(map(abs, m[0]))
        k = sum(map(abs, m[1]))
        e += p * k

print("Part 1:", e)

states = [set(), set(), set()]
periods = [-1, -1, -1]

n = 0
while True:

    for i in range(3):
        mi = tuple(tuple(c[i] for c in m) for m in moons)
        if mi in states[i] and periods[i] == -1:
            periods[i] = n
        states[i].add(mi)

    if all(p > 0 for p in periods):
        break

    n += 1

    for m1 in range(N):
        for m2 in range(m1 + 1, N):
            for i in range(3):
                if moons[m1][0][i] < moons[m2][0][i]:
                    moons[m1][1][i] += 1
                    moons[m2][1][i] -= 1
                elif moons[m1][0][i] > moons[m2][0][i]:
                    moons[m1][1][i] -= 1
                    moons[m2][1][i] += 1

    for m in range(N):
        for i in range(3):
            moons[m][0][i] += moons[m][1][i]

# print(periods)
print("Part 2:", np.lcm.reduce(periods))
