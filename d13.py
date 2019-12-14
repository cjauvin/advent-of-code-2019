from collections import defaultdict
import os
import time


def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt

        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty

    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


getch = _find_getch()


def decode_instruction(i):
    s = f"{i:05}"
    assert len(s) <= 5
    return tuple(map(int, [s[-2:], s[-3], s[-4], s[-5]]))


def execute(prog, n_quarters=2):
    # prog = list(map(int, source.split(",")))
    prog[0] = n_quarters
    prog = defaultdict(int, zip(range(len(prog)), prog))
    i = 0  # instruction pointer
    relative_base = 0

    def get_param(m, j):
        if m == 0:  # position
            return prog[prog[i + j]]
        elif m == 1:  # immediate
            return prog[i + j]
        elif m == 2:  # relative
            return prog[prog[i + j] + relative_base]
        else:
            assert False

    while True:
        opc, m1, m2, m3 = decode_instruction(prog[i])

        if opc in (1, 2):
            assert m3 in [0, 2]
            p1 = get_param(m1, 1)
            p2 = get_param(m2, 2)
            w3 = prog[i + 3] + (relative_base if m3 == 2 else 0)
            prog[w3] = p1 + p2 if opc == 1 else p1 * p2
            i += 4

        elif opc == 3:
            assert m1 in [0, 2]
            w3 = prog[i + 1] + (relative_base if m1 == 2 else 0)
            input_ = yield
            assert type(input_) is int, f"received invalid input: {input_}"
            # print(f"setting {input_} in {w3}")
            prog[w3] = input_
            i += 2

        elif opc == 4:
            out = get_param(m1, 1)
            # print(f"sending {out}")
            yield out
            i += 2

        elif opc in (5, 6):
            p1 = get_param(m1, 1)
            p2 = get_param(m2, 2)
            if opc == 5 and p1 != 0:
                i = p2
            if opc == 6 and p1 == 0:
                i = p2
            if i != p2:
                i += 3

        elif opc in (7, 8):
            assert m3 in [0, 2]
            p1 = get_param(m1, 1)
            p2 = get_param(m2, 2)
            w3 = prog[i + 3] + (relative_base if m3 == 2 else 0)
            if opc == 7:
                prog[w3] = 1 if p1 < p2 else 0
            elif opc == 8:
                prog[w3] = 1 if p1 == p2 else 0
            i += 4

        elif opc == 9:
            relative_base += get_param(m1, 1)
            i += 2

        elif opc == 99:
            break

        else:
            assert False

        assert i < len(prog)


def draw(g):
    os.system("clear")
    rows = []
    for y in range(23):
        rows.append([H[g[(x, y)]] for x in range(45)])
    print()
    for row in rows:
        print("".join(row))


H = {0: " ", 1: "X", 2: "#", 3: "=", 4: "o"}
g = {}

source = open("d13_input.txt").read()
prog = list(map(int, source.split(",")))
# for i in range(639, 639 + 1035):
#     if prog[i] == 2:
#         prog[i] = 0

# for i in range(639, 639 + 766 - (1 * 45)):
#     if prog[i] == 0:
#         prog[i] = 2

for i in range(639 + (21 * 45) + 1, 639 + (22 * 45) - 2):
    prog[i] = 3

run = execute(prog)
n_block_tiles = 0

data = []
for pixel in range(45 * 23):
    try:
        data.append((next(run), next(run), next(run)))
        if data[-1][2] == 2:
            n_block_tiles += 1
    except StopIteration:
        break

for x, y, t in data:
    g[(x, y)] = t

draw(g)

score = (next(run), next(run), next(run))
print(score)

next(run)

# joysticks = [0]  # , 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 0, 0, 1, 1, 1, 0, 0, 0, 0]
joysticks = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
joysticks = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

scores = []

# for joystick in joysticks:
while True:

    # time.sleep(0.0)
    joystick = 0
    # c = getch()
    # if c == "q":
    #     exit()
    # if c == "a":
    #     joystick = -1
    # elif c == "d":
    #     joystick = 1
    # else:
    #     joystick = 0

    try:
        accum = [run.send(joystick)]
        assert accum[0] != -1
        while True:
            a = next(run)
            if a != None:
                accum.append(a)
            else:
                break
            if len(accum) == 3:
                if accum[0] == -1:
                    assert accum[1] == 0
                    # print("Score:", accum[2])
                    scores.append(accum[2])
                else:
                    g[(accum[0], accum[1])] = accum[2]
                accum = []

        draw(g)
        if scores:
            print(scores[-1])

    except StopIteration:
        break

print(scores[-1])
