from collections import defaultdict
from intcode import intcode


robot = intcode(open("d17_input.txt").read())
g = defaultdict(lambda: " ")

chars = {46: ".", 35: "#", 10: "\n", 94: "?"}
g = defaultdict(lambda: ".")
x, y = 0, 0
width = float("-inf")
while True:
    try:
        c = chars[next(robot)]
        if c == "\n":
            g[(x, y)] = "\n"
            width = max(width, x)
            x = 0
            y += 1
        else:
            g[(x, y)] = c
            x += 1
    except StopIteration as e:
        break

height = y - 1

print()
sum_align_params = 0
for y in range(0, height):
    row = []
    for x in range(0, width):
        c = g[(x, y)]
        left = g[(x - 1, y)]
        right = g[(x + 1, y)]
        up = g[(x, y - 1)]
        down = g[(x, y + 1)]
        if {c, left, right, up, down} == {"#"}:
            row.append("O")
            sum_align_params += x * y
        else:
            row.append(c)
    print("".join(row))

print(f"Part 1: {sum_align_params}")
