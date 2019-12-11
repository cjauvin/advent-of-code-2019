from collections import defaultdict


def decode_instruction(i):
    s = f"{i:05}"
    assert len(s) <= 5
    return tuple(map(int, [s[-2:], s[-3], s[-4], s[-5]]))


def execute(source):
    prog = list(map(int, source.split(",")))
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
            prog[w3] = yield
            i += 2

        elif opc == 4:
            yield get_param(m1, 1)
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


def paint(initial_color):

    robot = execute(open("d11_input.txt").read())

    g = {}
    pos = (0, 0)
    g[pos] = initial_color
    d = "^"
    n_painted_once = 1

    dims = (float("inf"), float("-inf"), float("inf"), float("-inf"))

    while True:

        try:
            next(robot)  # advance to next input yield
            curr_color = g.get(pos, 0)
            next_color = robot.send(curr_color)  # first output
            turn = next(robot)  # second output
        except StopIteration:
            break

        if pos not in g:
            n_painted_once += 1

        g[pos] = next_color

        if d == "^":
            d = "<" if turn == 0 else ">"
        elif d == ">":
            d = "^" if turn == 0 else "v"
        elif d == "v":
            d = ">" if turn == 0 else "<"
        elif d == "<":
            d = "v" if turn == 0 else "^"

        if d == "^":
            pos = (pos[0], pos[1] - 1)
        elif d == ">":
            pos = (pos[0] + 1, pos[1])
        elif d == "v":
            pos = (pos[0], pos[1] + 1)
        elif d == "<":
            pos = (pos[0] - 1, pos[1])

        dims = (
            min(pos[0], dims[0]),
            max(pos[0], dims[1]),
            min(pos[1], dims[2]),
            max(pos[1], dims[3]),
        )

    return n_painted_once, g, dims


n_painted_once, _, _ = paint(0)

print("Part 1:", n_painted_once)

_, g, dims = paint(1)

print("Part 2:")

for y in range(dims[2], dims[3] + 1):
    print(
        "".join(
            [" " if g.get((x, y), 0) == 0 else "#" for x in range(dims[0], dims[1] + 1)]
        )
    )
