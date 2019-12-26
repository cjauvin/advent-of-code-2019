from collections import defaultdict
from intcode import intcode


def draw():
    extent = [float("inf"), float("-inf"), float("inf"), float("-inf")]
    for p in g.keys():
        extent = [
            min(extent[0], p[0]),
            max(extent[1], p[0]),
            min(extent[2], p[1]),
            max(extent[3], p[1]),
        ]
    # print(extent)
    for y in range(extent[2] - 1, extent[3] + 1):
        row = [g[(x, y)] for x in range(extent[0] - 1, extent[1] + 1)]
        print("".join(row))
    print()


def visit(pos, from_direction=None, steps=1):
    global robot, g
    assert g[pos] != "#"
    if g[pos] == " ":
        g[pos] = "."
    for direction in [1, 2, 3, 4]:
        if direction == 1:
            candidate_pos = (pos[0], pos[1] - 1)
        elif direction == 2:
            candidate_pos = (pos[0], pos[1] + 1)
        elif direction == 3:
            candidate_pos = (pos[0] - 1, pos[1])
        elif direction == 4:
            candidate_pos = (pos[0] + 1, pos[1])
        if g[candidate_pos] == " ":
            next(robot)
            answer = robot.send(direction)
            # print(pos, direction, answer)
            assert answer in [0, 1, 2]
            if answer == 0:
                g[candidate_pos] = "#"
            elif answer == 1:
                visit(candidate_pos, direction, steps + 1)
            elif answer == 2:
                g[candidate_pos] = "O"
                print(f"Part 1: found oxygen in {steps} steps at {candidate_pos}")
                visit(candidate_pos, direction, steps + 1)
    if from_direction:
        next(robot)
        answer = robot.send(opposite_dir[from_direction])
        assert answer == 1


robot = intcode(open("d15_input.txt").read())
g = defaultdict(lambda: " ")
opposite_dir = {1: 2, 2: 1, 3: 4, 4: 3}

visit((0, 0))

draw()

n_minutes = 0
while True:
    expanding = False
    for pos in [p for p, v in g.items() if v == "O"]:
        for direction in [1, 2, 3, 4]:
            if direction == 1:
                candidate_pos = (pos[0], pos[1] - 1)
            elif direction == 2:
                candidate_pos = (pos[0], pos[1] + 1)
            elif direction == 3:
                candidate_pos = (pos[0] - 1, pos[1])
            elif direction == 4:
                candidate_pos = (pos[0] + 1, pos[1])
            if g[candidate_pos] == ".":
                g[candidate_pos] = "O"
                expanding = True
    if not expanding:
        break
    n_minutes += 1

draw()

print(f"Part 2: filled with oxygen in {n_minutes} minutes")
