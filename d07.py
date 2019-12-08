import itertools

src = "3,8,1001,8,10,8,105,1,0,0,21,42,51,76,93,110,191,272,353,434,99999,3,9,1002,9,2,9,1001,9,3,9,1002,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,3,9,4,9,99,3,9,1002,9,4,9,101,5,9,9,1002,9,3,9,1001,9,4,9,1002,9,5,9,4,9,99,3,9,1002,9,5,9,101,3,9,9,102,5,9,9,4,9,99,3,9,1002,9,5,9,101,5,9,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99"


def decode_instruction(i):
    s = f"{i:05}"
    assert len(s) <= 5
    return tuple(map(int, [s[-2:], s[-3], s[-4], s[-5]]))


def execute(source):
    prog = list(map(int, source.split(",")))
    i = 0
    while True:
        opc, m1, m2, m3 = decode_instruction(prog[i])

        if opc in (1, 2):
            assert m3 == 0
            p1 = prog[prog[i + 1]] if m1 == 0 else prog[i + 1]
            p2 = prog[prog[i + 2]] if m2 == 0 else prog[i + 2]
            prog[prog[i + 3]] = p1 + p2 if opc == 1 else p1 * p2
            i += 4

        elif opc == 3:
            assert m1 == 0
            prog[prog[i + 1]] = yield
            i += 2

        elif opc == 4:
            out = prog[prog[i + 1]] if m1 == 0 else prog[i + 1]
            yield out
            i += 2

        elif opc in (5, 6):
            p1 = prog[prog[i + 1]] if m1 == 0 else prog[i + 1]
            p2 = prog[prog[i + 2]] if m2 == 0 else prog[i + 2]
            if opc == 5 and p1 != 0:
                i = p2
            if opc == 6 and p1 == 0:
                i = p2
            if i != p2:
                i += 3

        elif opc in (7, 8):
            assert m3 == 0
            p1 = prog[prog[i + 1]] if m1 == 0 else prog[i + 1]
            p2 = prog[prog[i + 2]] if m2 == 0 else prog[i + 2]
            if opc == 7:
                prog[prog[i + 3]] = 1 if p1 < p2 else 0
            elif opc == 8:
                prog[prog[i + 3]] = 1 if p1 == p2 else 0
            i += 4

        elif opc == 99:
            return

        else:
            assert False

        assert i < len(prog)


# src = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
# src = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
# src = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"


max_signal = float("-inf")
for perm in itertools.permutations(range(5)):
    amps = []
    signal = 0
    for phase in perm:
        amp = execute(src)
        next(amp)
        amp.send(phase)
        out = amp.send(signal)
        signal = out
    max_signal = max(max_signal, signal)
print("Part1:", max_signal)


# src = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
# src = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"

max_signal = float("-inf")
for perm in itertools.permutations(range(5, 10)):
    signal = 0
    amps = []
    for phase in perm:
        amp = execute(src)
        amps.append(amp)
        next(amp)
        amp.send(phase)
        out = amp.send(signal)
        signal = out

    halted = False
    while not halted:
        for amp in amps:
            try:
                next(amp)
            except StopIteration:
                halted = True
                break
            out = amp.send(signal)
            signal = out
        max_signal = max(max_signal, signal)

print("Part2:", max_signal)
