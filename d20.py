from collections import defaultdict
import re

s = """
         A
         A
  #######.#########
  #######.........#
  #######.#######.#
  #######.#######.#
  #######.#######.#
  #####  B    ###.#
BC...##  C    ###.#
  ##.##       ###.#
  ##...DE  F  ###.#
  #####    G  ###.#
  #########.#####.#
DE..#######...###.#
  #.#########.###.#
FG..#########.....#
  ###########.#####
             Z
             Z
"""

s_ = """
                   A
                   A
  #################.#############
  #.#...#...................#.#.#
  #.#.#.###.###.###.#########.#.#
  #.#.#.......#...#.....#.#.#...#
  #.#########.###.#####.#.#.###.#
  #.............#.#.....#.......#
  ###.###########.###.#####.#.#.#
  #.....#        A   C    #.#.#.#
  #######        S   P    #####.#
  #.#...#                 #......VT
  #.#.#.#                 #.#####
  #...#.#               YN....#.#
  #.###.#                 #####.#
DI....#.#                 #.....#
  #####.#                 #.###.#
ZZ......#               QG....#..AS
  ###.###                 #######
JO..#.#.#                 #.....#
  #.#.#.#                 ###.#.#
  #...#..DI             BU....#..LF
  #####.#                 #.#####
YN......#               VT..#....QG
  #.###.#                 #.###.#
  #.#...#                 #.....#
  ###.###    J L     J    #.#.###
  #.....#    O F     P    #.#...#
  #.###.#####.#.#####.#####.###.#
  #...#.#.#...#.....#.....#.#...#
  #.#####.###.###.#.#.#########.#
  #...#.#.....#...#.#.#.#.....#.#
  #.###.#####.###.###.#.#.#######
  #.#.........#...#.............#
  #########.###.###.#############
           B   J   C
           U   P   P
"""

s_ = """
             Z L X W       C
             Z P Q B       K
  ###########.#.#.#.#######.###############
  #...#.......#.#.......#.#.......#.#.#...#
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
  #.#...#.#.#...#.#.#...#...#...#.#.......#
  #.###.#######.###.###.#.###.###.#.#######
  #...#.......#.#...#...#.............#...#
  #.#########.#######.#.#######.#######.###
  #...#.#    F       R I       Z    #.#.#.#
  #.###.#    D       E C       H    #.#.#.#
  #.#...#                           #...#.#
  #.###.#                           #.###.#
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#
CJ......#                           #.....#
  #######                           #######
  #.#....CK                         #......IC
  #.###.#                           #.###.#
  #.....#                           #...#.#
  ###.###                           #.#.#.#
XF....#.#                         RF..#.#.#
  #####.#                           #######
  #......CJ                       NM..#...#
  ###.#.#                           #.###.#
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#
  #.....#        F   Q       P      #.#.#.#
  ###.###########.###.#######.#########.###
  #.....#...#.....#.......#...#.....#.#...#
  #####.#.###.#######.#######.###.###.#.#.#
  #.......#.......#.#.#.#.#...#...#...#.#.#
  #####.###.#####.#.#.#.#.###.###.#.###.###
  #.......#.....#.#...#...............#...#
  #############.#.#.###.###################
               A O F   N
               A A D   M
"""

g = defaultdict(lambda: " ")
portal_infos = defaultdict(
    list
)  # BC -> [(x0,y0,inside|outside), (x1,y1,inside|outside)]
portals = {}  # pos -> pos
inside_portals = {}  # pos at level N -> pos at level N + 1
outside_portals = {}  # pos at level N -> pos at level N - 1
portal_names = {}  # pos -> name

width = 0
y = -2

# input_source = s.split("\n")
input_source = open("d20_input.txt")

for line in input_source:
    line = line.rstrip()
    if not line:
        continue
    for x, c in enumerate(line, -2):
        if c in ["#", "."]:
            g[(x, y)] = c
            width = max(width, x + 1)
        elif c != " ":
            g[(x, y)] = c
    y += 1

height = y - 2

# print(width, height)

# horizontal portals
for y in range(-2, height + 2):
    is_outside = True
    for x in range(-2, width + 2):
        if g[(x, y)] in ["#", "."]:
            is_outside = not is_outside
        portal = g[(x, y)] + g[(x + 1, y)]
        if re.match("[A-Z]{2}", portal):
            if g[(x - 1, y)] == ".":
                portal_infos[portal].append(
                    (x - 1, y, "outside" if is_outside else "inside")
                )
            elif g[(x + 2, y)] == ".":
                portal_infos[portal].append(
                    (x + 2, y, "outside" if is_outside else "inside")
                )

# vertical portals
for x in range(-2, height + 2):
    is_outside = True
    for y in range(-2, height + 2):
        if g[(x, y)] in ["#", "."]:
            is_outside = not is_outside
        portal = g[(x, y)] + g[(x, y + 1)]
        if re.match("[A-Z]{2}", portal):
            if g[(x, y - 1)] == ".":
                portal_infos[portal].append(
                    (x, y - 1, "outside" if is_outside else "inside")
                )
            elif g[(x, y + 2)] == ".":
                portal_infos[portal].append(
                    (x, y + 2, "outside" if is_outside else "inside")
                )

for portal, ps in portal_infos.items():
    if len(ps) == 2:
        portals[ps[0][:2]] = ps[1][:2]
        portals[ps[1][:2]] = ps[0][:2]
        if ps[0][-1] == "inside":
            inside_portals[ps[0][:2]] = ps[1][:2]
            outside_portals[ps[1][:2]] = ps[0][:2]
            portal_names[ps[0][:2]] = f"{portal} (inside)"
            portal_names[ps[1][:2]] = f"{portal} (outside)"
        elif ps[0][-1] == "outside":
            outside_portals[ps[0][:2]] = ps[1][:2]
            inside_portals[ps[1][:2]] = ps[0][:2]
            portal_names[ps[0][:2]] = f"{portal} (outside)"
            portal_names[ps[1][:2]] = f"{portal} (inside)"


def draw():
    print()
    for y in range(height):
        print(
            "".join(g[(x, y)] if g[(x, y)] in ["#", "."] else " " for x in range(width))
        )


min_dists = defaultdict(lambda: float("inf"))  # (x, y) -> dist
min_dists_with_levels = defaultdict(lambda: float("inf"))  # (x, y, level) -> dist


def solve1():
    global min_dists
    to_visit = [(AA, 0)]
    while to_visit:
        p, dist = to_visit.pop()
        if dist >= min_dists[p]:
            continue
        min_dists[p] = dist
        for r in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            q = (p[0] + r[0], p[1] + r[1])
            if g[q] == ".":
                to_visit.append((q, dist + 1))
        if p in portals:
            to_visit.append((portals[p], dist + 1))


MAX_RECURSION_LEVEL = 25


def solve2():
    global min_dists_with_levels
    to_visit = [(AA0, 0)]
    while to_visit:
        p, dist = to_visit.pop()
        x, y, level = p
        if dist >= min_dists_with_levels[p] or level > MAX_RECURSION_LEVEL:
            continue
        min_dists_with_levels[p] = dist
        for r in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            q = (x + r[0], y + r[1])
            if g[q] == ".":
                to_visit.append(((q[0], q[1], level), dist + 1))
        if (x, y) in inside_portals:
            # print(f"reached {portal_names[(x, y)]} at dist {dist}")
            a = inside_portals[(x, y)]
            to_visit.append(((a[0], a[1], level + 1), dist + 1))
        if level > 0 and (x, y) in outside_portals:
            # print(f"reached {portal_names[(x, y)]} at dist {dist}")
            # exit()
            a = outside_portals[(x, y)]
            to_visit.append(((a[0], a[1], level - 1), dist + 1))


# draw()

AA = portal_infos["AA"][0][:2]
AA0 = (AA[0], AA[1], 0)
ZZ = portal_infos["ZZ"][0][:2]
ZZ0 = (ZZ[0], ZZ[1], 0)

solve1()
solve2()

print("Part 1:", min_dists[ZZ])
print("Part 2:", min_dists_with_levels[ZZ0])
