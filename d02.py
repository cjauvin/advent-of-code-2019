s = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,19,5,23,2,23,9,27,1,5,27,31,1,9,31,35,1,35,10,39,2,13,39,43,1,43,9,47,1,47,9,51,1,6,51,55,1,13,55,59,1,59,13,63,1,13,63,67,1,6,67,71,1,71,13,75,2,10,75,79,1,13,79,83,1,83,10,87,2,9,87,91,1,6,91,95,1,9,95,99,2,99,10,103,1,103,5,107,2,6,107,111,1,111,6,115,1,9,115,119,1,9,119,123,2,10,123,127,1,127,5,131,2,6,131,135,1,135,5,139,1,9,139,143,2,143,13,147,1,9,147,151,1,151,2,155,1,9,155,0,99,2,0,14,0"
# s = "1,9,10,3,2,3,11,0,99,30,40,50"

prog = list(map(int, s.split(",")))


def execute(prog, noun, verb):
    prog[1] = noun
    prog[2] = verb
    for i in range(0, len(prog), 4):
        # print(i, prog[i : i + 4])
        # print(prog)
        if prog[i] == 1:
            prog[prog[i + 3]] = prog[prog[i + 1]] + prog[prog[i + 2]]
        elif prog[i] == 2:
            prog[prog[i + 3]] = prog[prog[i + 1]] * prog[prog[i + 2]]
        elif prog[i] == 99:
            break
        else:
            assert False
        # print(prog)
        # print("---")
    return prog[0]


# Part 1
# print(execute(prog[:], 12, 2))

# Part 2
found = False
for noun in range(100):
    for verb in range(100):
        out = execute(prog[:], noun, verb)
        # print(noun, verb, out)
        if out == 19690720:
            print("found:", noun, verb, 100 * noun + verb)
            found = True
            break
    if found:
        break
