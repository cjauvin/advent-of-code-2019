from collections import defaultdict


def decode_instruction(i):
    s = f"{i:05}"
    assert len(s) <= 5
    return tuple(map(int, [s[-2:], s[-3], s[-4], s[-5]]))


def intcode(source):
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
            # print("waiting for input..")
            input_ = yield
            # print(f"received {input_}")
            assert type(input_) is int, f"received invalid input: {input_}"
            # print(f"setting {input_} in {w3}")
            prog[w3] = input_
            i += 2

        elif opc == 4:
            out = get_param(m1, 1)
            # print(f"outputting {out}")
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
