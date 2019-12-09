def decode_instruction(i):
    s = f"{i:05}"
    assert len(s) <= 5
    return tuple(map(int, [s[-2:], s[-3], s[-4], s[-5]]))


def execute(source, input_):
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
            prog[prog[i + 1]] = input_
            i += 2

        elif opc == 4:
            print(prog[prog[i + 1]] if m1 == 0 else prog[i + 1])
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
            break
        else:
            assert False

        assert i < len(prog)


# Part 1

# execute("3,0,4,0,99", 123)
execute(open("d05_input.txt").read(), 1)

# Part 2

# input < 8:  999
# input == 8: 1000
# input > 8:  1001
# execute(
#     "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99",
#     -100,
# )

execute(open("d05_input.txt").read(), 5)
