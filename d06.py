s = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""

s = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"""

tree = {}

# for line in s.split("\n"):
for line in open("d06_input.txt"):
    if not line.strip():
        continue
    a, b = line.strip().split(")")
    # print(f"{a}, {b}")
    tree[b] = a


def steps_to_com(a):
    steps = []
    while a != "COM":
        steps.append(a)
        a = tree[a]
    return steps


# assert len(steps_to_com("D")) == 3
# assert len(steps_to_com("L")) == 7
# assert len(steps_to_com("COM")) == 0

# # Part 1
n = 0
for k in tree.keys():
    n += len(steps_to_com(k))

print(n)

# print(steps_to_com("YOU"))
# print(steps_to_com("SAN"))

# Part 2

you = set(steps_to_com("YOU")[1:])
san = set(steps_to_com("SAN")[1:])

print(len((san | you) - (san & you)))
