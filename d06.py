tree = {}

for line in open("d06_input.txt"):
    inner, outer = line.strip().split(")")
    tree[outer] = inner


def steps_to_com(o):
    steps = set()
    while o != "COM":
        steps.add(o := tree[o])  # warning this is Py3.8+ only!
    return steps


print("Part 1:", sum(len(steps_to_com(o)) for o in tree.keys()))

you = steps_to_com("YOU")
san = steps_to_com("SAN")

print("Part 2:", len((san | you) - (san & you)))
