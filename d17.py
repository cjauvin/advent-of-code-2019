from collections import defaultdict
from intcode import intcode


# prog = list(map(int, open("d17_input.txt").read().split(",")))
# robot = intcode(prog)
# g = defaultdict(lambda: " ")

# chars = {46: ".", 35: "#", 10: "\n", 94: "?"}
# g = defaultdict(lambda: ".")
# x, y = 0, 0
# width = float("-inf")
# while True:
#     try:
#         c = chars[next(robot)]
#         if c == "\n":
#             g[(x, y)] = "\n"
#             width = max(width, x)
#             x = 0
#             y += 1
#         else:
#             g[(x, y)] = c
#             x += 1
#     except StopIteration as e:
#         break

# height = y - 1

# print()
# sum_align_params = 0
# for y in range(0, height):
#     row = []
#     for x in range(0, width):
#         c = g[(x, y)]
#         left = g[(x - 1, y)]
#         right = g[(x + 1, y)]
#         up = g[(x, y - 1)]
#         down = g[(x, y + 1)]
#         if {c, left, right, up, down} == {"#"}:
#             row.append("O")
#             sum_align_params += x * y
#         else:
#             row.append(c)
#     print("".join(row))

# # print(f"Part 1: {sum_align_params}")


# def get_next(pos, d):
#     if d == "^":
#         return (pos[0], pos[1] - 1)
#     elif d == "v":
#         return (pos[0], pos[1] + 1)
#     elif d == "<":
#         return (pos[0] - 1, pos[1])
#     elif d == ">":
#         return (pos[0] + 1, pos[1])


# dirs = ["^", ">", "v", "<"]
# di = 0
# n = 0
# pos = (0, 12)
# commands = []
# while True:
#     if g[get_next(pos, dirs[di])] == "#":
#         # keep going
#         n += 1
#         pos = get_next(pos, dirs[di])
#     elif g[get_next(pos, dirs[(di + 1) % 4])] == "#":
#         # turn right
#         di += 1
#         di %= 4
#         if n > 0:
#             commands.append(str(n))
#         n = 0
#         commands.append("R")
#     elif g[get_next(pos, dirs[(di - 1) % 4])] == "#":
#         # turn left
#         di -= 1
#         di %= 4
#         if n > 0:
#             commands.append(str(n))
#         n = 0
#         commands.append("L")
#     else:
#         break

# commands.append(str(n))

# print(",".join(commands))

A = "R,6,L,10,R,10,R,10\n"
B = "L,10,L,12,R,10\n"
C = "R,6,L,12,L,10\n"
main = "A,B,A,B,A,C,A,C,B,C\n"

# robot = intcode(open("d17_input.txt").read())

# R,6,L,10,R,10,R,10, L,10,L,12,R,10, R,6,L,10,R,10,R,10, L,10,L,12,R,10, R,6,L,10,R,10,R,10, R,6,L,12,L,10, R,6,L,10,R,10,R,10, R,6,L,12,L,10, L,10,L,12,R,10, R,6,L,12,L,10
# A                   B               A                   B               A                   C              A                   C              B               C

# A: R,6,L,10,R,10,R,10
# B: L,10,L,12,R,10
# C: R,6,L,12,L,10

prog = list(map(int, open("d17_input.txt").read().split(",")))
prog[0] = 2
robot = intcode(prog, False)

while True:
    c = chr(next(robot))
    print(c, end="")
    if c == ":":
        break

print()
next(robot)
next(robot)

for c in main:
    robot.send(ord(c))

while True:
    c = chr(next(robot))
    print(c, end="")
    if c == ":":
        break

print()
next(robot)
next(robot)

for c in A:
    robot.send(ord(c))

while True:
    c = chr(next(robot))
    print(c, end="")
    if c == ":":
        break

print()
next(robot)
next(robot)

for c in B:
    robot.send(ord(c))

while True:
    c = chr(next(robot))
    print(c, end="")
    if c == ":":
        break

print()
next(robot)
next(robot)

for c in C:
    robot.send(ord(c))

while True:
    c = chr(next(robot))
    print(c, end="")
    if c == "?":
        break

print()
next(robot)
next(robot)

robot.send(ord("n"))
robot.send(ord("\n"))

while True:
    try:
        a = next(robot)
    except StopIteration as e:
        break

print(a)
